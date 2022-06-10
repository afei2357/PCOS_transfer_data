from app import db
from datetime import datetime

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Reports(PaginatedAPIMixin,db.Model):
    __tablename__ = 'reports'
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lis_Barcode = db.Column(db.String(64))
    info = db.Column(db.String(500))
    create_time = db.Column(db.DateTime)
    clazz = db.Column(db.String(20)) # 类别
    update_time  = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)

    def from_dict(self, data):
        columns = self.__table__.columns.keys()
        for field in columns:
            if field in data:
                if isinstance(data[field],str):
                    setattr(self, field, data[field].strip())
                else:
                    setattr(self, field, data[field])
        self.update_time = datetime.now()

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'create_time' or key == 'update_time' :
                value = getattr(self, key).strftime("%Y-%m-%d")
            else:
                value = getattr(self, key)
            result[key] = value
        return result







