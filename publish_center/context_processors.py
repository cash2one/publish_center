from account.models import User
from express.models import PublishTask
from publish_center.api import *
import settings


def name_proc(request):
    user_total_num = User.objects.all().count()
    user_active_num = User.objects.filter(is_active=True).count()
    apply_num = PublishTask.objects.filter(status=2).count()
    request.session.set_expiry(3600)

    info_dic = {
                'user_total_num': user_total_num,
                'user_active_num': user_active_num,
                'apply_num': apply_num,
                }

    return info_dic
