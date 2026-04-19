from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ItemForm
from .models import Item
from .services import recommend_matches


CATEGORY_LABELS = dict(Item.CATEGORY_CHOICES)
TYPE_LABELS = dict(Item.TYPE_CHOICES)


def home(request):
    q = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or "").strip()
    item_type = (request.GET.get("type") or "").strip()
    sort = (request.GET.get("sort") or "new").strip()

    base_qs = Item.objects.select_related("user")
    qs = base_qs

    if item_type in {Item.TYPE_LOST, Item.TYPE_FOUND}:
        qs = qs.filter(type=item_type)

    if category:
        qs = qs.filter(category=category)

    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(location__icontains=q)
        )

    if sort == "time":
        qs = qs.order_by("-time")
    else:
        qs = qs.order_by("-created_at")

    filtered_count = qs.count()
    items = qs[:30]
    today = timezone.localdate()

    top_categories = []
    for row in (
        base_qs.values("category").annotate(c=Count("id")).order_by("-c")[:4]
    ):
        top_categories.append(
            {
                "value": row["category"],
                "label": CATEGORY_LABELS.get(row["category"], row["category"]),
                "count": row["c"],
            }
        )

    stats = {
        "total": base_qs.count(),
        "open": base_qs.filter(status=Item.STATUS_OPEN).count(),
        "closed": base_qs.filter(status=Item.STATUS_CLOSED).count(),
        "today": base_qs.filter(created_at__date=today).count(),
        "lost": base_qs.filter(type=Item.TYPE_LOST).count(),
        "found": base_qs.filter(type=Item.TYPE_FOUND).count(),
        "filtered": filtered_count,
    }

    return render(
        request,
        "items/home.html",
        {
            "items": items,
            "q": q,
            "category": category,
            "type": item_type,
            "sort": sort,
            "categories": Item.CATEGORY_CHOICES,
            "stats": stats,
            "top_categories": top_categories,
        },
    )


def item_detail(request, pk: int):
    item = get_object_or_404(Item.objects.select_related("user"), pk=pk)

    opposite_type = Item.TYPE_FOUND if item.type == Item.TYPE_LOST else Item.TYPE_LOST
    candidates = (
        Item.objects.filter(type=opposite_type, status=Item.STATUS_OPEN)
        .exclude(pk=item.pk)
        .order_by("-created_at")[:200]
    )
    matches = recommend_matches(item, candidates)

    return render(
        request,
        "items/detail.html",
        {"item": item, "matches": matches, "match_count": len(matches)},
    )


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "信息发布成功。")
            return redirect("item_detail", pk=obj.pk)
    else:
        initial = {}
        preset_type = (request.GET.get("type") or "").strip()
        if preset_type in {Item.TYPE_LOST, Item.TYPE_FOUND}:
            initial["type"] = preset_type
        form = ItemForm(initial=initial)

    return render(request, "items/form.html", {"form": form, "mode": "create"})


@login_required
def item_edit(request, pk: int):
    item = get_object_or_404(Item, pk=pk)
    if item.user_id != request.user.id and not request.user.is_staff:
        messages.error(request, "你没有权限执行该操作。")
        return redirect("item_detail", pk=item.pk)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "信息已更新。")
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, "items/form.html", {"form": form, "mode": "edit", "item": item})


@login_required
def item_delete(request, pk: int):
    item = get_object_or_404(Item, pk=pk)
    if item.user_id != request.user.id and not request.user.is_staff:
        messages.error(request, "你没有权限执行该操作。")
        return redirect("item_detail", pk=item.pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "信息已删除。")
        return redirect("home")

    return render(request, "items/delete.html", {"item": item})


@login_required
def my_items(request):
    item_qs = Item.objects.filter(user=request.user).select_related("user").order_by("-created_at")
    stats = {
        "total": item_qs.count(),
        "open": item_qs.filter(status=Item.STATUS_OPEN).count(),
        "closed": item_qs.filter(status=Item.STATUS_CLOSED).count(),
    }
    items = item_qs[:50]
    return render(request, "items/my_items.html", {"items": items, "stats": stats})


@login_required
def item_close(request, pk: int):
    item = get_object_or_404(Item, pk=pk)
    if item.user_id != request.user.id and not request.user.is_staff:
        messages.error(request, "你没有权限执行该操作。")
        return redirect("item_detail", pk=item.pk)

    item.status = Item.STATUS_CLOSED
    item.save(update_fields=["status", "updated_at"])
    messages.success(request, "该信息已标记为完成。")
    return redirect("item_detail", pk=item.pk)


def _is_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(_is_staff)
def admin_dashboard(request):
    today = timezone.localdate()
    base = Item.objects.select_related("user")
    total_count = base.count()

    stats = {
        "today_count": base.filter(created_at__date=today).count(),
        "closed_count": base.filter(status=Item.STATUS_CLOSED).count(),
        "open_count": base.filter(status=Item.STATUS_OPEN).count(),
        "total_count": total_count,
    }
    stats["completion_rate"] = (
        round(stats["closed_count"] * 100 / total_count) if total_count else 0
    )

    by_category = []
    for row in base.values("category").annotate(c=Count("id")).order_by("-c"):
        by_category.append(
            {
                "value": row["category"],
                "label": CATEGORY_LABELS.get(row["category"], row["category"]),
                "count": row["c"],
                "percent": round(row["c"] * 100 / total_count) if total_count else 0,
            }
        )

    by_type = []
    for row in base.values("type").annotate(c=Count("id")).order_by("-c"):
        by_type.append(
            {
                "value": row["type"],
                "label": TYPE_LABELS.get(row["type"], row["type"]),
                "count": row["c"],
                "percent": round(row["c"] * 100 / total_count) if total_count else 0,
            }
        )

    recent_items = base.order_by("-created_at")[:6]

    return render(
        request,
        "items/admin_dashboard.html",
        {
            "stats": stats,
            "by_category": by_category,
            "by_type": by_type,
            "recent_items": recent_items,
        },
    )
