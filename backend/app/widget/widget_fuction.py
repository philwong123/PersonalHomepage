import datetime
import logging

from ..base_model import Base
from ..common_func import CommonFunc
from ..login.login_funtion import User

from ..model.widget_model import widget_suite
from ..model.widget_model import widget as widget_table

cf = CommonFunc()
logger = logging.getLogger(__name__)


class Widget(Base):
    id = None
    name = None
    name_zh = None
    is_valid = None
    span = None
    buttons = None
    auto_update = None
    update_time = None

    def __init__(self, name=None, name_zh=None, is_valid=None, span=None, buttons=None, auto_update=0, update_time=datetime.datetime.now(), id=0):
        self.name = name
        self.name_zh = name_zh
        self.is_valid = is_valid
        self.span = span
        self.buttons = buttons
        self.auto_update = auto_update
        self.update_time = update_time
        self.id = id

    def complete(self):
        _ = widget_table.get(widget_table.id == self.id)
        self.name = _.name
        self.name_zh = _.name_zh
        self.is_valid = _.is_valid
        self.span = _.span
        self.buttons = _.buttons
        self.auto_update = _.auto_update
        self.update_time = _.update_time
        return self


def widget_suite_get(user_id):
    logger.debug(f"Getting widget suite for user_id: {user_id}")
    return [{
        'id': s_['id'],
        'name': s_['name'],
        'order': s_['order'],
        'detail': eval(s_['detail']),
        'update_time': s_['update_time']
    } for s_ in widget_suite.select().where((widget_suite.user_id == user_id) & (widget_suite.is_valid == 1)).order_by(widget_suite.order).dicts()]


def widget_suite_delete(user_id):
    try:
        widget_suite.update(is_valid=0, update_time=datetime.datetime.now()).where((widget_suite.user_id == user_id) & (widget_suite.is_valid == 1)).execute()
        return True, 'success'
    except Exception as e:
        return False, e


def widget_get(user_id, suite_id):
    try:
        logger.debug(f"Getting widget for user_id={user_id}, suite_id={suite_id}")
        _ = widget_suite.get(widget_suite.id == suite_id)
        
        if int(_.user_id) != int(user_id):
            logger.warning(f"User {user_id} tried to access suite {suite_id} belonging to user {_.user_id}")
            return []
            
        widget_id_list = eval(_.detail)
        logger.debug(f"Found widget_id_list: {widget_id_list}")
        
        result = []
        for widget_id in widget_id_list:
            try:
                widget = Widget(id=widget_id).complete()
                if widget is not None:
                    result.append(cf.attr_to_dict(widget))
                else:
                    logger.warning(f"Widget {widget_id} not found")
            except Exception as e:
                logger.error(f"Error processing widget {widget_id}: {str(e)}")
                
        logger.debug(f"Returning {len(result)} widgets")
        return result
        
    except widget_suite.DoesNotExist:
        logger.error(f"Widget suite {suite_id} not found")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in widget_get: {str(e)}")
        raise


def widget_all():
    return [{
        'id': _['id'],
        'name': _['name'],
        'name_zh': _['name_zh'],
        'span': _['span'],
        'buttons': eval(_['buttons']),
        'auto_update': _['auto_update'],
        'update_time': _['update_time']
    } for _ in widget_table.select().where(widget_table.is_valid == 1).dicts()]
