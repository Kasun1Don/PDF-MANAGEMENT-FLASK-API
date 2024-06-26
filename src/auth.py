from init import db

def admin_only():
    @jwt_required
    def inner():
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if user:
            return fn()
        return 
    


# ensure that the JWT use is the owner of the document
