# Standard library imports
import os
from typing import List, NamedTuple

# 3rd party imports
from google.cloud import bigquery
import pandas as pd

# Local imports
import Credentials as c
from database.db_consts import TableCols, Cond


class DatabaseInterface:
    """Provides interface layer between bot and BigQuery.

    Designed to house all necessary component methods for interfacing with
    Google's BigQuery. Handles query generation from `tag` input, query
    execution, and structuring data into a usable format. No functionality
    outside BigQuery interfacing and query manipulation is offered--this should
    instead be handled by a more specific controller.

    This class is relatively generalized, but contains some project-specific
    features/artifacts to ensure viability and efficiency for the duration
    of this project.

    Constants:
        BASE_LINK: const str URI to gitbot BigQuery dataset
        DB_URI: (const str) URI link to gitbot dataset on BigQuery
        SO_URI: (const str) URI link to stackoverflow dataset on BigQuery

    Attributes:
        client: BigQuery client for access to BigQuery tables
        name_map: dict mapping long-form URIs to shortened URIs

            Long-form URIs are a single long string containing the
            BigQuery project reference name, dataset name, table name, and
            column name. Short-form URIs are generated as

                    '{table/tag name}_{column name}'

            where 'table/tag name' refers to a table/tag with proceeding 'git-'
            or 'git_' removed. 'column name' refers to a given column within
            the provided table. These shortened URIs are of the form that would
            be used during a 'SELECT _ AS _' statement.
    """

    BASE_LINK = "`elated-nectar-258022.gitbot.{tbl_name}{col}`"
    DB_URI = "elated-nectar-258022.gitbot"
    SO_URI = "elated-nectar-258022.stackoverflow"

    def __init__(self):
        """Init bq client for database access."""
        self.client = bigquery.Client()
        self.name_map = {}

    def format_selects(self, selects: List[TableCols]) -> List[str]:
        """Formats a list of tables/columns to select from."""
        statements: List[str] = []

        for ntup in selects:
            table: str = ntup.table.replace('-', '_')

            for col in ntup.cols:
                statements.append(self._format_select(ntup.uri, table, col))

        return statements

    def _format_select(self, uri, tbl, col) -> str:
        """Formats a single simple query."""

        # If selecting all, don't need to specify columns
        if col != '*':
            stmt = " ".join([
                "`{}.{}`.{}".format(uri, tbl, col),
                "AS",
                self.shorten_colname(uri, tbl, col)
            ])

        else:
            stmt = "*"

        return stmt

    def format_wheres(self, comps: List[Cond]) -> List[str]:
        """Formats queries containing a 'where' clause.

        :param comps: list of (first, comparison, second) tuples
        :return:
        """
        wheres: List[str] = []

        # Loop through each 'WHERE' statement
        for cond in comps:
            # Formats first element of the condition
            fst = self.shorten_colname(
                cond.fst.uri, cond.fst.table, cond.fst.cols) \
                if isinstance(cond.fst, TableCols) else cond.fst
            # Check to see if 'WHERE' is binary or unary
            if cond.snd:
                # If binary, formats second element of the condition
                snd = self.shorten_colname(
                    cond.snd.uri, cond.snd.table, cond.snd.cols) \
                    if isinstance(cond.snd, TableCols) else cond.snd
                # Composes final statement as {first} {comparison} {second}
                wheres.append("{} {} {}".format(fst, cond.comparison, snd))
            else:
                # If unary, simply returns {first} {comparison}
                # E.g. WHERE table.xyz NOT NULL
                wheres.append("{} {}".format(fst, cond.comparison))

        return wheres

    def format_ons(self, ons: str) -> str:
        """Formats 'ON' statements (for a JOIN) to keep syntax consistency."""

        # Generalized use case; if >1, ensure all are in name_map and
        # replace each long-form URI with a shortened one.
        if isinstance(ons, list):
            on_split = {x for on in ons for x in on.split(" ") if self.DB_URI in x}
            replaced = []

            # Put unmapped long-form URIs into name_map.
            for unmapped in on_split - set(self.name_map.keys()):
                split = unmapped.split('.')
                uri, tbl, col = split[:-2], split[-2], split[-1]
                _ = self.shorten_colname(uri, tbl, col)

            # Replace every long-form URI in each string with its respective
            # shortened identifier.
            for on in ons:
                repl = on
                split = on.split(' ')
                for s in split:
                    if s in self.name_map.keys():
                        repl = repl.replace(s, self.name_map['s'])

                replaced.append(repl)

        # Just one str; replace all long-form URIs with shortened ones.
        else:
            replaced = ons
            split = ons.split(' ')

            for s in split:
                if s not in self.name_map.keys():
                    uri, tbl, col = split[:-2], split[-2], split[-1]
                    _ = self.shorten_colname(uri, tbl, col)

                replaced = replaced.replace(s, self.name_map['s'])

        return replaced

    def shorten_colname(self, uri: str, tbl: str, col: str) -> str:
        """Generates a shortened reference for a table and column.

        :param uri: BigQuery URI to dataset
        :param tbl: table name within dataset
        :param col: column name within table
        :return:
        """
        colname = "_".join([
            "_".join(tbl.split('_')[1:]),
            col
        ])

        try:
            if not self.name_map[uri] == colname:
                self.name_map[uri] = colname
        except KeyError:
            self.name_map[uri] = colname

        return colname


    def run_query(self, query: str) -> pd.DataFrame:
        """Send query to BigQuery, wait for result, then return as DataFrame."""
        query_job = self.client.query(
            query,
            location="US"
        )

        result = query_job.result()
        return result.to_dataframe()

    def template_query(self, selects: List[str], froms: str,
                       wheres: List[str]=None) -> str:
        """Generates generic inner join query from template.

        :param qparams: namedtuple containing necessary info
        :return:
        """
        # If more than one "ON" condition, join by "AND"

        if wheres:
            query = (
                " SELECT "
                "{selects}"
                " FROM "
                "`{froms}` "
                " WHERE "
                "{wheres} "
            ).format(
                selects=", ".join(selects),
                froms=froms,
                wheres=" AND ".join(wheres)
            )

        else:
            query = (
                " SELECT "
                    "{selects}"
                " FROM "
                    "`{froms}` "
            ).format(
                selects=", ".join(selects),
                froms=froms
            )

        return query

    def template_query_ijoin(self, selects: List[str], froms: str,
                             join: str, ons: str or List[str]) -> str:
        """Generates generic inner join query from template.

        :param qparams: namedtuple containing necessary info
        :return:
        """
        # If more than one "ON" condition, join by "AND"
        ons = " AND ".join(ons) if isinstance(ons, list) else ons

        query = (
            " SELECT "
                "{selects}"
            " FROM "
                "`{froms}`"
            " INNER JOIN "
                "`{join}`"
            " ON "
                "{ons}"
        ).format(
            selects=", ".join(selects),
            froms=froms,
            join=join,
            ons=ons
        )

        return query

    def get_post_answers(self, tag: str) -> pd.DataFrame:
        """Gets post and accepted answer title/body from BigQuery.

        :param tag: the SO tag for the table to pull from.
        :return: DataFrame with columns for post/answer title and body.
        """
        ans_link = "{}".format(".".join([self.SO_URI, 'git_answers']))

        # if isinstance(tags, list):
        #     table_tups = [TableCols(self.DB_URI, tag, ['title', 'body'])
        #                   for tag in tags]
        # else:
        table_tups = TableCols(self.DB_URI, tag, ['title', 'body'])

        selects = self.format_selects([table_tups])
        ons = "`{tbl_from}`.accepted_answer_id = `{tbl_ansr}`.id".format(
            tbl_from='.'.join([self.DB_URI, tag]),
            tbl_ansr=ans_link
        )

        # Generate inner join template and run query on BigQuery.
        results = self.run_query(self.template_query_ijoin(selects=selects,
                                          froms=".".join([self.DB_URI, tag]),
                                          join=ans_link,
                                          ons=ons))

        return results

    def generic_query(self, parameters: TableCols,
                      comps: List[Cond]=None) -> pd.DataFrame:
        """Allows for generic querying (uri/table/columns) to BigQuery.

        Note: BigQuery access through this method currently only supports
        execution of a single query (as a single TableCols NamedTuple) per call.

        :param parameters: contains URI link, table, and columns of interest
        :return: DataFrame of resultant query information
        """
        selects = self.format_selects([parameters])
        if not comps is None:
            wheres = self.format_wheres(comps)
            query = self.template_query(
                selects=selects,
                froms=".".join([parameters.uri,parameters.table]),
                wheres=wheres)
        else:
            query = self.template_query(
                selects=selects,
                froms=".".join([parameters.uri, parameters.table]))
        results = self.run_query(query)
        return results

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = c.GOOGLE_APPLICATION_CREDENTIALS
    interface = DatabaseInterface()
    q1 = TableCols(uri='elated-nectar-258022.stackoverflow',
                  table='git_tags',
                  cols=['tag_name'])

    results1 = interface.generic_query(q1)
    print(results1)

    print('\n\n')

    results2 = interface.get_post_answers('git_add')
    print(results2)

    q3c = TableCols(uri='elated-nectar-258022.gitbot',
                  table='git_add',
                  cols=['*'])
    q3w = [
        Cond('accepted_answer_id', 'IS NOT NULL', ''),
        Cond('score', '> 3', '')
    ]

    result3 = interface.generic_query(q3c, q3w)
    print(result3)