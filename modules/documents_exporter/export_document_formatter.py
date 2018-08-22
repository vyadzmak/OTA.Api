def get_width_with_new_line(value):
    try:
        lines = value.split('\n')
        l = 0
        for line in lines:
            if (len(line) > l):
                l = len(line)

        return l
        pass
    except Exception as e:
        pass


def get_column_widths(data):
    try:
        widths = []
        rows = data[1]
        row_index = 0
        k = 0.7
        for row in rows:
            cell_index = 0
            for cell in row:
                if (row_index == 0):
                    # value =cell

                    if ('\n' in str(cell)):
                        width = get_width_with_new_line(cell) * k
                        widths.append(width)
                    else:
                        width = len(cell) * k
                        widths.append(width)

                else:

                    if ('\n' in str(cell)):
                        l = get_width_with_new_line(cell) * k
                        if (widths[cell_index] < l):
                            widths[cell_index] = l

                    else:
                        if (widths[cell_index] < len(cell) * k):
                            widths[cell_index] = len(cell) * k

                cell_index += 1
            row_index += 1
        t = 0

        rows = data[0]
        row_index = 0
        k = 1.2
        _widths = []
        for row in rows:
            cell_index = 0
            for cell in row:
                if (row_index == 0):
                    # value =cell

                    if ('\n' in str(cell)):
                        width = get_width_with_new_line(cell) * k
                        _widths.append(width)
                    else:
                        width = len(cell) * k
                        _widths.append(width)

                else:

                    if ('\n' in str(cell)):
                        l = get_width_with_new_line(cell) * k
                        if (_widths[cell_index] < l):
                            _widths[cell_index] = l

                    else:
                        if (_widths[cell_index] < len(cell) * k):
                            _widths[cell_index] = len(cell) * k

                cell_index += 1
            row_index += 1

        if (len(widths) == len(_widths)):
            i = 0
            for w in widths:

                if (_widths[i] > w):
                    widths[i] = _widths[i]
                i += 1

        min_width = 10
        max_width =50
        index = 0
        for width in widths:
            if (width < min_width):
                widths[index] = min_width

            if (width>max_width):
                widths[index] = max_width

            index += 1
        return widths
        pass
    except Exception as e:

        pass


def generate_header_styles():
    pass


def generate_text_style(workbook):
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    return cell_format
    pass


def generate_double_style(workbook):
    cell_format = workbook.add_format()
    cell_format.set_num_format('#,##0.00')
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    return cell_format
    pass


def generate_date_style(workbook):
    formatdict = {'num_format': 'mm/dd/yyyy'}
    cell_format = workbook.add_format(formatdict)
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    return cell_format
    pass


def generate_worksheet_styles(workbook, worksheet, names):
    try:
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y']

        index = 0

        for name in names:
            column = columns[index] + ':' + columns[index]
            if (name == 'period'):
                worksheet.set_column(column, None, generate_date_style(workbook))

            if (
                                        name == 'document' or name == 'account' or name == 'analyticsDebet' or name == 'analyticsCredit' or name == 'accountDebet' or name == 'accountCredit' or name == 'typeName'):
                worksheet.set_column(column, None, generate_text_style(workbook))

            if (
                                                name == 'valueDebet' or name == 'valueCredit' or name == 'startPeriodBalanceDebet' or name == 'startPeriodBalanceCredit' or name == 'periodTransactionsDebet' or name == 'periodTransactionsCredit' or name == 'endPeriodBalanceDebet' or name == 'endPeriodBalanceCredit' or name == ''):
                worksheet.set_column(column, None, generate_double_style(workbook))

            index += 1
            pass

        pass
    except Exception as e:
        pass
