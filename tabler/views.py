import decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from datetime import date, datetime

from inventory.models import Asset
from tabler.forms import (
    TableBTypeForm, TableBForm, TableBActiveFilterForm, TableBActiveForm, TableBActiveOrderForm,
    TableBActiveSplitForm, TableBActiveAskFinishForm, TableBActiveFinishForm)
from tabler.models import (
    TableBType, TableB, TableBActive, TableBActiveOrder, TableBActiveOrderTmp, TableBActiveSplit,
    TableBActiveSplitOrder, TableBActiveBill, TableBActiveFinish)


# Create your views here.
class TableBTypeAll(LoginRequiredMixin, ListView):
    template_name = 'tabler/TableBType/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_count'] = get_user_model().objects.all().count()
        context['TableBTypes'] = TableBType.objects.order_by('id')
        return context


class TableBTypeNew(LoginRequiredMixin, CreateView):
    model = TableBType
    template_name = 'tabler/TableBType/create.html'
    form_class = TableBTypeForm
    login_url = 'manager:login'
    success_url = reverse_lazy('tabler:tab_type_all')


class TableBTypeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'tabler/TableBType/edit.html'
    form_class = TableBTypeForm
    login_url = 'manager:login'
    model = TableBType
    success_url = reverse_lazy('tabler:tab_type_all')


# TableB's Controller
class TableBNew(LoginRequiredMixin, CreateView):
    model = TableB
    form_class = TableBForm
    template_name = 'tabler/TableB/create.html'
    login_url = 'manager:login'
    success_url = reverse_lazy('tabler:tab_all')


class TableBAll(LoginRequiredMixin, ListView):
    template_name = 'tabler/TableB/overview.html'
    model = TableB
    login_url = 'manager:login'
    context_object_name = 'tablebs'
    paginate_by = 10


class TableBView(LoginRequiredMixin, DetailView):
    queryset = TableB.objects.select_related('type')
    template_name = 'tabler/TableB/single.html'
    context_object_name = 'tableb'
    login_url = 'manager:login'


class TableBUpdate(LoginRequiredMixin, UpdateView):
    model = TableB
    template_name = 'tabler/TableB/edit.html'
    form_class = TableBForm
    login_url = 'manager:login'

    # success_url = reverse_lazy('tabler:tab_all')
    def get_success_url(self):
        return reverse('tabler:tab_view', kwargs={'pk': self.kwargs['pk']})


class TableBDelete(LoginRequiredMixin, DeleteView):
    pass


def tablebactive_overview(request):
    # mobile = request.GET.get('mobile')
    # fname = request.GET.get('fname')
    tablebactives = TableBActive.objects.all()

    context = {
        'form': TableBActiveFilterForm(),
        'tab_acts': tablebactives.order_by('-id')
    }
    return render(request, 'tabler/TableBActive/overview.html', context)


"""
class TableBActiveNew(LoginRequiredMixin, CreateView):
    model = TableBActive
    form_class = TableBActiveForm
    template_name = 'tabler/TableBActive/create.html'
    login_url = 'manager:login'
    success_url = reverse_lazy('tabler:tab_all')
"""


def get_last_rec_in_table_active(cur_pk):
    select = None
    n = TableBActive.objects.all().count()
    i = n
    while i <= n:
        rec = TableBActive.objects.get(id=i)
        if rec.table_name_id == cur_pk:
            if not rec.done:
                select = rec
                break
        i -= 1

    if select is None:
        return None
    else:
        return select


def do_input_current_time(input_data):
    current_datetime = datetime.now()
    if input_data is not None:
        input_time = str(input_data)
        today = date.today()
        current_datetime = datetime(
            today.year, today.month, today.day,
            int(input_time[:2]), int(input_time[3:5])
        )
    return current_datetime


class TableBActiveNew(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'tabler/TableBActive/open_table.html'
    model = TableBActive
    form_class = TableBActiveForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('tabler:tab_act_ok', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()

        if form.is_valid():

            current_datetime = do_input_current_time(form.cleaned_data['time_input'])

            TableBActive.objects.create(
                table_name_id=self.kwargs['pk'],
                time_start=current_datetime,
                note=form.cleaned_data['note']
            )

            rec = TableB.objects.get(id=self.kwargs['pk'])
            rec.active = True
            rec.active_time = current_datetime
            rec.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        if 'pk' in self.kwargs:
            # select = get_last_table_active(self.kwargs['pk'])

            tableb = TableB.objects.get(pk=self.kwargs['pk'])
            context['tableb'] = tableb
            context['tablebtype'] = TableBType.objects.get(id=tableb.type_id)
            # context['tablebactive'] = select
            return context
        else:
            return context


def calc_minutes_between_times(time_s, time_e):
    time_end = datetime.strptime(str(time_e)[11:16], "%H:%M")
    time_start = datetime.strptime(str(time_s)[11:16], "%H:%M")
    if time_end.hour >= time_start.hour:
        total_minutes = int((time_end - time_start).total_seconds() / 60)
    else:
        yesterday_minutes = (24 * 60) - (time_start.hour * 60) - time_start.minute
        total_minutes = yesterday_minutes + time_end.hour * 60 + time_end.minute

    return total_minutes


class TableBActiveOK(LoginRequiredMixin, ListView):
    template_name = 'tabler/TableBActive/active.html'
    model = get_user_model()
    login_url = 'manager:login'

    def get_context_data(self, **kwargs):
        select = get_last_rec_in_table_active(self.kwargs['pk'])
        # tab_act_orders = TableBActiveOrder.objects.filter(table_active=select.id).order_by('order_asset__name')
        tab_act_orders = TableBActiveOrder.objects.filter(table_active=select.id)

        TableBActiveOrderTmp.objects.all().delete()
        cur_id = 0
        ass_sum = 0
        for tab_order in tab_act_orders:
            cur_id += 1
            ass_price = tab_order.order_asset.price
            ass_quantity = tab_order.quantity
            ass_sum += ass_price * ass_quantity
            TableBActiveOrderTmp.objects.create(
                id=cur_id,
                asset_id=tab_order.order_asset.id,
                asset_name=tab_order.order_asset.name,
                asset_price=ass_price,
                asset_quantity=ass_quantity,
                asset_sum=ass_price * ass_quantity
            )

        tab_act = TableB.objects.get(id=self.kwargs['pk'])

        orders = TableBActiveOrder.objects.filter(table_active=select.id)

        splits = TableBActiveSplit.objects.filter(table_active=select.id)

        TableBActiveBill.objects.all().delete()

        last_time = select.time_start
        key_id = 0
        for split in splits:
            split_minutes = calc_minutes_between_times(last_time, split.split_time)

            time_start = str(last_time.hour) + ':' + str(last_time.minute)
            time_ended = str(split.split_time.hour) + ':' + str(split.split_time.minute)

            key_id += 1
            TableBActiveBill.objects.create(
                id=key_id,
                product='- Cơ ' + str(split.pk)
                        + ' [' + time_start
                        + '] - [' + time_ended + ']',
                quantity=None,
                price=None,
                paid=split_minutes * tab_act.type.cost
            )

            order_details = TableBActiveSplitOrder.objects.filter(split_table=split.id)
            total_paid = split_minutes * tab_act.type.cost
            for order_detail in order_details:
                cur_ass = Asset.objects.get(id=order_detail.order_asset)
                order_paid = order_detail.quantity * cur_ass.price
                total_paid += order_paid

                key_id += 1
                TableBActiveBill.objects.create(
                    id=key_id,
                    product=cur_ass.name[:18],
                    quantity=order_detail.quantity,
                    price=cur_ass.price,
                    paid=order_paid
                )

                # if total_paid == split.split_paid:
            key_id += 1
            TableBActiveBill.objects.create(
                id=key_id,
                product='Tổng tiền cơ ' + str(split.pk),
                quantity=None,
                price=None,
                paid=total_paid
            )

            last_time = split.split_time

        total_minutes = calc_minutes_between_times(tab_act.active_time, datetime.now())

        tab_type = TableBType.objects.get(id=tab_act.type_id)

        curr_co = splits.count() + 1
        curr_time = datetime.now()
        curr_time_paid = calc_minutes_between_times(last_time, curr_time) * tab_act.type.cost
        key_id += 1
        TableBActiveBill.objects.create(
            id=key_id,
            product='- Cơ ' + str(curr_co)
                    + ' [' + str(last_time.hour) + ':' + str(last_time.minute)
                    + '] - [' + str(curr_time.hour) + ':' + str(curr_time.minute) + ']',

            quantity=None,
            price=None,
            paid=curr_time_paid
        )

        curr_order_paid = 0
        for order in orders:
            if order.quantity_remain > 0:
                ord_pay = order.quantity_remain * order.order_asset.price
                key_id += 1
                TableBActiveBill.objects.create(
                    id=key_id,
                    product=order.order_asset.name[:18],
                    quantity=order.quantity_remain,
                    price=order.order_asset.price,
                    paid=ord_pay
                )
                curr_order_paid += ord_pay

        key_id += 1
        TableBActiveBill.objects.create(
            id=key_id,
            product='Tổng tiền cơ ' + str(curr_co),
            quantity=None,
            price=None,
            paid=curr_order_paid + curr_time_paid
        )

        """
        key_id += 1
        TableBActiveBill.objects.create(
            id=key_id,
            product='Tiền giờ từ '
                    + str(last_time.hour) + ':' + str(last_time.minute)
                    + ' đến '
                    + str(curr_time.hour) + ':' + str(curr_time.minute)
            ,
            quantity=None,
            price=None,
            paid=(tab_type.cost * total_minutes)
        )
        """

        key_id += 1
        TableBActiveBill.objects.create(
            id=key_id,
            product='TỔNG CỘNG',
            quantity=None,
            price=None,
            paid=ass_sum + (tab_type.cost * total_minutes)
        )

        context = super().get_context_data(**kwargs)
        context['Tab_Assets'] = TableBActiveOrderTmp.objects.all()
        context['Sum_Price'] = ass_sum

        context['TableBs'] = TableB.objects.all()
        context['TableAct'] = tab_act
        context['TableBActives'] = TableBActive.objects.all()
        context['TableBActSelect'] = select
        context['TotalMinutes'] = total_minutes
        context['Price'] = tab_type.cost
        context['Pay'] = tab_type.cost * total_minutes
        context['TableBActiveOrders'] = tab_act_orders
        context['Total_Paid'] = ass_sum + (tab_type.cost * total_minutes)
        context['Splits'] = splits
        context['Orders'] = orders
        context['Bills'] = TableBActiveBill.objects.all()
        return context


class TableBActOrder(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'tabler/TableBActive/order.html'
    model = TableBActiveOrder
    form_class = TableBActiveOrderForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('tabler:tab_act_ok', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()

        if form.is_valid():
            select = get_last_rec_in_table_active(self.kwargs['pk'])

            tab_act = select.id
            if tab_act > 0:
                qty = form.cleaned_data['quantity']
                if int(qty) > 0:
                    TableBActiveOrder.objects.create(
                        table_active=tab_act,
                        order_asset=form.cleaned_data['order_asset'],
                        quantity=qty,
                        quantity_remain=qty,
                        order_time=datetime.now(),
                    )
            else:
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            tableb = TableB.objects.get(pk=self.kwargs['pk'])
            context['tableb'] = tableb
            context['tablebtype'] = TableBType.objects.get(id=tableb.type_id)
            return context
        else:
            return context


class TableBActSplit(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'tabler/TableBActive/split.html'
    model = TableBActiveSplit
    form_class = TableBActiveSplitForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('tabler:tab_act_ok', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()

        if form.is_valid():
            select = get_last_rec_in_table_active(self.kwargs['pk'])

            tab_act = select.id
            if tab_act > 0:
                orders = (TableBActiveOrder.objects.filter(table_active=select.id)
                          .filter(quantity_remain__gt=0)
                          .order_by('order_asset_id', 'quantity_remain')
                          )

                order_paid = 0
                cur_ass = -1
                for order in orders:
                    if order.order_asset_id != cur_ass:
                        i_qty = request.POST.get(order.order_asset.name)
                        input_quantity = 0
                        if i_qty is not None:
                            input_quantity = int(i_qty)
                        if input_quantity > 0:
                            order_paid += input_quantity * order.order_asset.price
                            TableBActiveSplitOrder.objects.update_or_create(
                                split_table=TableBActiveSplit.objects.count() + 1,
                                order_asset=order.order_asset.id,
                                quantity=input_quantity
                            )
                        cur_ass = order.order_asset_id

                    if input_quantity <= order.quantity_remain:
                        order.quantity_remain -= input_quantity
                    else:
                        input_quantity -= order.quantity_remain
                        order.quantity_remain = 0

                    order.save(update_fields=['quantity_remain'])

                last_active_time = select.time_start

                # Get all records has saved the active times
                has_activated = TableBActiveSplit.objects.filter(table_active=tab_act).filter(done=False)

                if has_activated is not None:
                    for rec in has_activated:
                        if rec == has_activated.last():
                            last_active_time = rec.split_time

                input_time = do_input_current_time(form.cleaned_data['time_input'])
                spit_minutes = calc_minutes_between_times(last_active_time, input_time)
                total_paid = order_paid + (spit_minutes * select.table_name.type.cost)
                TableBActiveSplit.objects.create(
                    table_active=tab_act,
                    split_time=input_time,
                    split_paid=total_paid
                )

            else:
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            select = get_last_rec_in_table_active(self.kwargs['pk'])
            # orders = TableBActiveOrder.objects.filter(table_active=select.id)
            orders = (TableBActiveOrder.objects.filter(table_active=select.id)
                      .order_by('order_asset_id')
                      .values('order_asset__name')
                      .annotate(quantity=Sum('quantity'), quantity_remain=Sum('quantity_remain'))
                      )

            tableb = TableB.objects.get(pk=self.kwargs['pk'])
            context['tableb'] = tableb
            context['tablebtype'] = TableBType.objects.get(id=tableb.type_id)
            context['Orders'] = orders
            return context
        else:
            return context


class TableBActAskFinish(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'tabler/TableBActive/ask_finish.html'
    model = TableBActiveFinish
    form_class = TableBActiveAskFinishForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('tabler:tab_act_ok', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()

        if form.is_valid():
            current_datetime = do_input_current_time(form.cleaned_data['time_input'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            tableb = TableB.objects.get(pk=self.kwargs['pk'])
            context['tableb'] = tableb
            context['tablebtype'] = TableBType.objects.get(id=tableb.type_id)
            return context
        else:
            return context


class TableBActFinish(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'tabler/TableBActive/finish.html'
    model = TableBActiveFinish
    form_class = TableBActiveFinishForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('tabler:tab_act_ok', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()

        if form.is_valid():
            select = get_last_rec_in_table_active(self.kwargs['pk'])

            tab_act = select.id
            if tab_act > 0:
                qty = form.cleaned_data['quantity']
                if int(qty) > 0:
                    TableBActiveOrder.objects.create(
                        table_active=tab_act,
                        order_asset=form.cleaned_data['order_asset'],
                        quantity=qty,
                        quantity_remain=qty,
                        order_time=datetime.now(),
                    )
            else:
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            tableb = TableB.objects.get(pk=self.kwargs['pk'])
            context['tableb'] = tableb
            context['tablebtype'] = TableBType.objects.get(id=tableb.type_id)
            return context
        else:
            return context
