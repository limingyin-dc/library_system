from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import PurchaseOrder
from .forms import PurchaseOrderForm


@login_required
def purchase_list(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    qs = PurchaseOrder.objects.all().order_by('-created_at')
    status = request.GET.get('status', '')
    q = request.GET.get('q', '')
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(book_title__icontains=q)
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'purchase/purchase_list.html', {
        'page_obj': page, 'status': status, 'q': q,
        'status_choices': PurchaseOrder.STATUS_CHOICES
    })


@login_required
def purchase_create(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('purchase_list')
    form = PurchaseOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '采购记录添加成功')
        return redirect('purchase_list')
    return render(request, 'purchase/purchase_form.html', {'form': form, 'title': '新增采购'})


@login_required
def purchase_edit(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('purchase_list')
    order = get_object_or_404(PurchaseOrder, pk=pk)
    form = PurchaseOrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, '采购记录更新成功')
        return redirect('purchase_list')
    return render(request, 'purchase/purchase_form.html', {'form': form, 'title': '编辑采购'})


@login_required
def purchase_delete(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('purchase_list')
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, '采购记录删除成功')
        return redirect('purchase_list')
    return render(request, 'confirm_delete.html', {'obj': order, 'cancel_url': reverse('purchase_list')})
