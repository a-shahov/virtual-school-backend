from virtual_school_backend import db


class Main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return (
            f'description: {self.description}'
        )


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
         return (
            f'title: {self.title}\n'
        )
