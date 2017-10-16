#---------------------------------- DataFrame Utils ----------------------------------#

import pandas as pd

class DataframeUtils(object):
    
    @classmethod
    def get_cuc_from_doc_in_df(cls, df, column_doctype, column_doc, column_cuc):
        """
        Returns the variable CUC (Series) based on the type and the number of the documents.
        df: Dataframe.
        column_doctype: (str) Column name of the document type.
        column_doc: (str) Column name of the document number.
        column_cuc: (str) Column name for storing the CUC.
        """
        df[column_cuc] = df[column_doctype].map(str) + '-' + df[column_doc].map(str)
        return df
    
    @classmethod
    def n_values(cls, df, cols = None, n = 6):
        """
        Returns a DataFrame with the first 'n' values by each columns.
        df: Dataframe.
        cols: (str, list) Column(s) name for describing.
        n: (int) Parameter for showing first 'n' values.
        """
        if cols is None:
            cols = df.columns
        elif isinstance(cols, str):
            cols = [cols]
#        N_cols = ['N_' + col for col in cols]
#        cols2 = np.asarray([cols, N_cols]).ravel(order = 'F')
        df_tmp = pd.DataFrame(columns = cols)
        for col in cols:
            firstn = df[col].value_counts().iloc[:n]
            firstn_index = firstn.index.tolist()
            firstn_N = firstn.values.tolist()
            for i in range(n - len(firstn)):
                firstn_index.append('')
                firstn_N.append(0)
            df_tmp[col] = ['{} ({:,})'.format(x, y) for x, y in zip(firstn_index, firstn_N)]
            df_tmp = df_tmp.applymap(str)
            df_tmp = df_tmp.applymap(lambda x: x.replace('(0)', ''))
            df_tmp.index = ['V' + str(x) for x in range(1, n + 1)]
        return df_tmp.T
    
    @classmethod
    def descrip_colmuns(cls, df, cols = None, n_vals = 6, summary = True):
        """
        Returns a DataFrame with descriptives like, dtype, N° Nulls,
        most frequency values, mean, etc by each column.
        df: Dataframe.
        cols: (str, list) Column(s) name for describing.
        n: (int) Parameter for showing first 'n' values.
        summary: (bool) Show Descriptive statistics ?
        """
        if cols is None:
            cols = df.columns
        df2 = df[cols].copy()
        dc = df2.dtypes.to_frame()
        dc.columns = ['dtype']
        dc['dtype'] = dc['dtype'].astype(str)
        dc['Tipo'] = ''
        dc['Tipo'][dc['dtype'] == 'object'] = 'Categoria'
        dc['Tipo'][[x.startswith(('int', 'float')) for x in dc['dtype']]] = 'Numero'
        n_nulls = df2.isnull().sum()#.to_frame('N_Nulls')
        n_nulls_porc = n_nulls / float(len(df2))
        a = pd.Series(['{} ({:.1%})'.format(x, y) for x, y in zip(n_nulls, n_nulls_porc)],
                       index = df2.columns, name = 'N_Nulls')
        dc = dc.join(a)
        dc = dc.join(df2.nunique().to_frame('N_Unicos'))
        if n_vals > 0:
            dc = dc.join(cls.n_values(df2, cols, n_vals))
        if summary:
            dc = dc.join(df2.describe().T)
        dc.fillna('', inplace = True)
        return dc
        
    @classmethod
    def print_basic_info(cls, df):
        """
        Returns a basic infor of a dataframe like the nrows, ncols, and the columns.
        df: Dataframe.
        """
        try:
            namespace = globals()
            df_name = [name for name in namespace if namespace[name] is df][0]
        except:
            df_name = ''
        shape = '{:,}'.format(df.shape[0]) + ' | ' + '{:,}'.format(df.shape[1])
        print('{} ({}):\n'.format(df_name, shape),list(df.columns))

    @classmethod
    def rolling_mean(cls, df, columns, column_id, n = 0, min_periods = 3):
        """
        Returns a DataFrame with the rolling mean of some columns.
        df: Dataframe.
        columns: (str, list) Column names to apply the rolling mean.
        column_id: (str, list) Column names to use as a grouper.
        n: Window for the rolling. 0 is equivalent to a rolling historical mean.
        min_periods: Minimum number of periods to show the rolling.
        """
#        group_by_data = df.set_index(column_id, append=True).groupby(level=1)
#        resulting_series_with_mean = group_by_data[columns].apply(
#            pd.rolling_mean, n, 1).reset_index(column_id)
        if isinstance(columns, str):
            columns = [columns]
        if isinstance(column_id, str):
            column_id = [column_id]
        ent = columns + column_id
        if n > 0:
            return df[ent].groupby(column_id).rolling(min_periods=min_periods,window=n).\
                   mean().reset_index(drop=True)[columns]
        else:
            return df[ent].groupby(column_id).expanding(min_periods=min_periods).\
                   mean().reset_index(drop=True)[columns]
        #resulting_series_with_mean[columns]

    @classmethod
    def rolling_sum(cls, df, columns, column_id, n = 0, min_periods = 3):
        """
        Returns a DataFrame with the rolling sum of some columns.
        df: Dataframe.
        columns: (str, list) Column names to apply the rolling sum.
        column_id: (str, list) Column names to use as a grouper.
        n: Window for the rolling. 0 is equivalent to a rolling historical sum.
        min_periods: Minimum number of periods to show the rolling.
        """
#        group_by_data = df.set_index(column_id, append=True).groupby(level=1)
#        resulting_series_with_mean = group_by_data[columns].apply(
#            pd.rolling_mean, n, 1).reset_index(column_id)
#        return resulting_series_with_mean[columns]
        if isinstance(columns, str):
            columns = [columns]
        if isinstance(column_id, str):
            column_id = [column_id]
        ent = columns + column_id
        if n > 0:
            return df[ent].groupby(column_id).rolling(min_periods=min_periods,window=n).\
                   sum().reset_index(drop=True)[columns]
        else:
            return df[ent].groupby(column_id).expanding(min_periods=min_periods).\
                   sum().reset_index(drop=True)[columns]

    @classmethod
    def get_categorical_columns(cls, df, columns_to_exclude = []):
        """
        Returns a list with the categorical columns.
        df: Dataframe.
        columns_to_exclude: (str, list) Column names to exclude (like IDs, Target, text, descriptions, etc).
        """
        if isinstance(columns_to_exclude, str):
            columns_to_exclude = [columns_to_exclude]
        return \
            [x for x in list(df.select_dtypes(include=['object', 'category']))
             if x not in columns_to_exclude]

    @classmethod
    def get_numerical_columns(cls, df, columns_to_exclude = []):
        """
        Returns a list with the numerical columns.
        df: Dataframe.
        columns_to_exclude: (str, list) Column names to exclude (like IDs, Target, text, descriptions, etc).
        """
        if isinstance(columns_to_exclude, str):
            columns_to_exclude = [columns_to_exclude]
        return \
            [x for x in list(df.select_dtypes(include=['integer', 'floating']))
             if x not in columns_to_exclude]

    @classmethod
    def get_columns_by_types(cls, df, columns_to_exclude = [], ordinal_columns = [],
                             print_flag=False):
        """
        Returns a tuple with the valid, categorical, numerical and nomial columns.
        Example: cols, cols_cat, cols_num, cols_nom = ra_df.get_columns_by_types(df, columns_to_exclude, ordinal_columns, print_flag = True)
        df: Dataframe.
        columns_to_exclude: (str, list) Column names to exclude (like IDs, Target, text, descriptions, etc).
        ordinal_columns: (str, list) Column names of the ordinal variables.
        """
        if isinstance(columns_to_exclude, str):
            columns_to_exclude = [columns_to_exclude]
        if isinstance(ordinal_columns, str):
            columns_to_exclude = [ordinal_columns]
        valid_columns = [x for x in df.columns if x not in columns_to_exclude]
        categorical_columns = \
            cls.get_categorical_columns(df, columns_to_exclude)
        numerical_columns = \
            cls.get_numerical_columns(df, columns_to_exclude)
        other_columns = \
            [x for x in valid_columns if x not in categorical_columns
             and x not in numerical_columns]
        nominal_columns = \
            [x for x in categorical_columns if x not in ordinal_columns]

        if print_flag:
            print('Categorical:\n', categorical_columns)
            print('\nCategorical - Ordinal:\n', ordinal_columns)
            print('\nCategorical - Nominal:\n', nominal_columns)
            print('\nNumerical:\n', numerical_columns)
            print('\nOther:\n', other_columns)
            print('\nExclude:\n', columns_to_exclude)

        return valid_columns, categorical_columns, \
               numerical_columns, nominal_columns

#---------------------------------- Format Utils ----------------------------------#
class FormatUtils(object):

    __str_date_format = '%d/%m/%Y'

    __dict_datetimes = {}
    __dict_dateints = {}

    @classmethod
    def get_year(cls, period):
        """
        Returns the year of a period.
        period: (int) Period.
        """
        return period // 100

    @classmethod
    def get_month(cls, period):
        """
        Returns the month of a period.
        period: (int) Period.
        """
        return period % 100

    @classmethod
    def gap_in_months_for_periods(cls, period_1, period_2):
        """
        Returns the number of month missed between two periods.
        period_1: (int) First period.
        period_2: (int) Second period.
        """
        year_1 = cls.get_year(period_1)
        year_2 = cls.get_year(period_2)
        month_1 = cls.get_month(period_1)
        month_2 = cls.get_month(period_2)

        if year_1 == year_2:
            basic_difference = abs(month_1 - month_2) - 1
            if basic_difference < 0:
                basic_difference = 0
            return basic_difference
        elif year_1 > year_2:
            greater_year_dif = month_1
            smaller_year_dif = 12 - month_2
            basic_difference = greater_year_dif + smaller_year_dif
            additional_months_difference = (year_1 - year_2 - 1) * 12
            return basic_difference + additional_months_difference - 1
        elif year_1 < year_2:
            greater_year_dif = month_2
            smaller_year_dif = 12 - month_1
            basic_difference = greater_year_dif + smaller_year_dif
            additional_months_difference = (year_2 - year_1 - 1) * 12
            return basic_difference + additional_months_difference - 1

    @classmethod
    def get_difference_in_months(cls, datetime1, datetime2, dif_base_on_days = False):
        """
        Returns the difference (int) from two datetimes:
        datetime1: (datetime) First datetime.
        datetime2: (datetime) Second datetime.
        dif_base_on_days: Should the difference be based on the exact dates or \
        based on the months and years of the dates.
        """
        if dif_base_on_days:
            difference = datetime1 - datetime2
            difference = abs(difference)
            return difference.days//30
        else:
            dif_years = datetime1.year - datetime2.year
            dif_months = datetime1.month - datetime2.month
            return abs(dif_years*12 + dif_months)

    @classmethod
    def date_to_integer(cls, raw_date, format_date = None, format_integer = '%Y%m'):
        """
        Return an integer in format (YYYYMM by default) of a date.
        raw_date: Date to convert.
        format_date: (str pattern) Format of the raw_date. Default -> automatic detection.
        format_integer: (str pattern) Format required to of the conversion. (YYYYMM by default) 
        """
#        if raw_date in cls.__dict_dateints:
#            return cls.__dict_dateints[raw_date]
#        else:
#            datetime_obj = datetime.strptime(raw_date, cls.__str_date_format)
#            if datetime_obj.month > 9:
#                current_month = datetime_obj.month
#            else:
#                current_month = '0'+str(datetime_obj.month)
#
#            formatted_date = '{year}{month}'.format(year=datetime_obj.year,
#                                                    month=current_month)
#            integer_date = int(formatted_date)
#            cls.__dict_dateints[raw_date] = integer_date
#            return integer_date
        return pd.to_datetime(raw_date, format=format_date).strftime(format_integer)
    
    @classmethod
    def make_datetime(cls, string_series, format=None, dayfirst=True):
        """
        Return a datetime series or string formated by a pattern.
        string_series: (str,series) Object to convert.
        format: (str pattern) Format of the object.
        dayfirst: Should the string_series have the day first ?
        """
        if isinstance(string_series, str):
            if len(string_series) == 6:
                string_series = str(string_series) + '01'
            return pd.to_datetime(string_series, format=format, dayfirst=dayfirst)
        else:
            if len(string_series[0]) == 6:
                string_series = string_series.map(lambda x: str(x) + '01')
            dates = {date:pd.to_datetime(date, format=format, dayfirst=dayfirst) for date in string_series.unique()}
            return string_series.map(dates)

#    @classmethod
#    def get_datetime(cls, raw_date):
#        if raw_date in cls.__dict_datetimes:
#            return cls.__dict_datetimes[raw_date]
#        else:
#            new_datetime = datetime.strptime(raw_date, cls.__str_date_format)
#            cls.__dict_datetimes[raw_date] = new_datetime
#            return new_datetime
