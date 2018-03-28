
import logging
import datetime

from guillotina import configure
from guillotina.browser import Response
from guillotina.transactions import commit
from .content import ILink

logger = logging.getLogger("api")


@configure.service(
    context=ILink, name='@check', method='POST',
    permission='guillotina.AccessContent'
)
async def check_link(context, request):
    print(context.last_checked)
    #logger.debug("haha")
    context.last_checked = datetime.datetime.today()
    await commit(request)
    return Response(response=dict(result="ok"), status=201)