__author__ = "ayazurrashid"
import re
from copy import deepcopy
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend
import  operator


class DatatablesFilterBackend(BaseFilterBackend):
    """
    Filter that works with datatables params.
    """
    def filter_queryset(self, request, queryset, view):
        try:
            custom_search_fields = view.custom_search_fields
            custom_order_fields = view.custom_order_fields
        except:
            custom_search_fields = None
            custom_order_fields = None

        if request.accepted_renderer.format != 'datatables':
            return queryset

        total_count = view.get_queryset().count()

        if len(getattr(view, 'filter_backends', [])) > 1:
            # case of a view with more than 1 filter backend
            filtered_count_before = queryset.count()
        else:
            filtered_count_before = total_count

        # set the queryset count as an attribute of the view for later
        setattr(view, '_datatables_total_count', total_count)

        # parse params
        if request.method == 'POST':
            request_data = request.data
        else:
            request_data = request.query_params
        getter = request_data.get
        if custom_search_fields:
            fields = self.get_custom_fields(getter, custom_search_fields)
            ordering = self.get_custom_ordering(getter, custom_order_fields)
        else:
            fields = self.get_fields(getter)
            ordering = self.get_ordering(getter, fields)
        search_value = getter('search[value]')
        search_regex = getter('search[regex]') == 'true'

        # filter queryset
        q = Q()
        for f in fields:
            if not f['searchable']:
                continue
            if search_value and search_value != 'false':
                search_value = search_value.lstrip().rstrip()
                if search_regex:
                    if self.is_valid_regex(search_value):
                        # iterate through the list created from the 'name'
                        # param and create a string of 'ior' Q() objects.
                        for x in f['name']:
                            q |= Q(**{'%s__iregex' % x: search_value})
                else:
                    # same as above.
                    for x in f['name']:
                        q |= Q(**{'%s__icontains' % x: search_value})
            f_search_value = f.get('search_value')
            f_search_regex = f.get('search_regex') == 'true'
            if f_search_value:
                if f_search_regex:
                    if self.is_valid_regex(f_search_value):
                        # create a temporary q variable to hold the Q()
                        # objects adhering to the field's name criteria.
                        temp_q = Q()
                        for x in f['name']:
                            temp_q |= Q(**{'%s__iregex' % x: f_search_value})
                        # Use deepcopy() to transfer them to the global Q()
                        # object. Deepcopy() necessary, since the var will be
                        # reinstantiated next iteration.
                        q = q & deepcopy(temp_q)
                else:
                    temp_q = Q()
                    for x in f['name']:
                        temp_q |= Q(**{'%s__icontains' % x: f_search_value})
                    q = q & deepcopy(temp_q)

        if q:
            queryset = queryset.filter(q).distinct()
            filtered_count = queryset.count()
        else:
            filtered_count = filtered_count_before
        # set the queryset count as an attribute of the view for later
        setattr(view, '_datatables_filtered_count', filtered_count)
        # order queryset
        queryset = queryset.distinct()
        if len(ordering):
            if hasattr(view, 'datatables_additional_order_by'):
                additional = view.datatables_additional_order_by
                # Django will actually only take the first occurrence if the
                # same column is added multiple times in an order_by, but it
                # feels cleaner to double check for duplicate anyway.
                if not any((o[1:] if o[0] == '-' else o) == additional
                           for o in ordering):
                    ordering.append(additional)

            queryset = self.order_queryset(ordering, queryset)

        return queryset

    def order_queryset(self, ordering, queryset):
        """

        :param ordering:
        :param queryset:
        :return:
        """
        # if ordering[0].strip('-') == 'id':
        #     queryset = list(queryset)
        #     queryset = sorted(queryset, key=lambda obj: obj.full_name,
        #                       reverse=True if '-' in ordering[0] else False)
        #
        # elif ordering[0].strip('-') == 'full_name':
        #     queryset = list(queryset)
        #     queryset = sorted(queryset, key=lambda obj: obj.full_name,
        #                       reverse=True if '-' in ordering[0] else False)
        #
        # elif ordering[0].strip('-') == 'email':
        #     queryset = list(queryset)
        #     queryset = sorted(queryset, key=lambda obj: obj.email,
        #                       reverse=True if '-' in ordering[0] else False)
        # elif ordering[0].strip('-') == 'mobile_number':
        #     queryset = list(queryset)
        #     queryset = sorted(queryset, key=lambda obj: obj.mobile_number,
        #                       reverse=True if '-' in ordering[0] else False)
        # elif ordering[0].strip('-') == 'address':
        #     queryset = list(queryset)
        #     queryset = sorted(queryset, key=lambda obj: obj.address,
        #                       reverse=True if '-' in ordering[0] else False)

        if True:
            try:
                queryset = queryset.order_by(*ordering)
            except Exception as e:
                pass
        return queryset

    def get_fields(self, getter):
        fields = []
        i = 0
        while True:
            col = 'columns[%d][%s]'
            data = getter(col % (i, 'data'))
            if data == "":  # null or empty string on datatables (JS) side
                fields.append({'searchable': False, 'orderable': False})
                i += 1
                continue
            # break out only when there are no more fields to get.
            if data is None:
                break
            name = getter(col % (i, 'name'))
            if not name:
                name = data
            search_col = col % (i, 'search')
            # to be able to search across multiple fields (e.g. to search
            # through concatenated names), we create a list of the name field,
            # replacing dot notation with double-underscores and splitting
            # along the commas.
            field = {
                'name': [
                    n.lstrip() for n in name.replace('.', '__').split(',')
                ],
                'data': data,
                'searchable': getter(col % (i, 'searchable')) == 'true',
                'orderable': getter(col % (i, 'orderable')) == 'true',
                'search_value': getter('%s[%s]' % (search_col, 'value')),
                'search_regex': getter('%s[%s]' % (search_col, 'regex')),
            }
            fields.append(field)
            i += 1
        return fields

    def get_custom_fields(self, getter, custom_search_fields):
        fields = []
        for fd in custom_search_fields:
            i = fd[1]
            col = 'columns[%d][%s]'
            data = getter(col % (i, 'data'))
            if data == "":  # null or empty string on datatables (JS) side
                fields.append({'searchable': False, 'orderable': False})
                continue
            # break out only when there are no more fields to get.
            if data is None:
                break
            name = getter(col % (i, 'name'))
            if not name:
                name = data
            search_col = col % (i, 'search')
            # to be able to search across multiple fields (e.g. to search
            # through concatenated names), we create a list of the name field,
            # replacing dot notation with double-underscores and splitting
            # along the commas.
            field = {
                'name': [fd[0]],
                'data': data,
                'searchable': getter(col % (i, 'searchable')) == 'true',
                'search_value': getter('%s[%s]' % (search_col, 'value')),
                'search_regex': getter('%s[%s]' % (search_col, 'regex')),
            }
            fields.append(field)
        return fields

    def get_custom_ordering(self, getter, custom_order_fields):
        ordering = []
        col = 'order[%d][%s]'
        dir_ = getter(col % (0, 'dir'), 'asc')
        column_ = getter(col % (0, 'column'), None)
        if column_ is not None:
            for fd in custom_order_fields:
                if int(column_) == fd[1]:
                    ordering.append('%s%s' % (
                        '-' if dir_ == 'desc' else '',
                        fd[0]
                    ))

        return ordering

    def get_ordering(self, getter, fields):
        ordering = []
        i = 0
        while True:
            col = 'order[%d][%s]'
            idx = getter(col % (i, 'column'))
            if idx is None:
                break
            try:
                field = fields[int(idx)]
            except IndexError:
                i += 1
                continue
            if not field['orderable']:
                i += 1
                continue
            dir_ = getter(col % (i, 'dir'), 'asc')
            ordering.append('%s%s' % (
                '-' if dir_ == 'desc' else '',
                field['name'][0]
            ))
            i += 1
        return ordering

    def is_valid_regex(cls, regex):
        try:
            re.compile(regex)
            return True
        except re.error:
            return False