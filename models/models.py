from db import db
import datetime



class ParkingModel(db.Model):
    __tablename__ = 'parkings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    service_cost = db.Column(db.Float(precision=2))
    service_cost_balance = db.Column(db.Float(precision=2))

    rentals = db.relationship('RentalModel', lazy='dynamic')

    def __init__(self, name, address, price):
        self.name = name
        self.address = address
        self.price = price
        self.service_cost = None
        self.service_cost_balance = None


    def json(self):
        return {'name':self.name, 'address':self.address, 'price':self.price}


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        object = ParkingModel.query.filter_by(id=self.id).first()
        object.name = self.name
        object.address = self.address
        object.price = self.price
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def parking_list(cls, page):
        return cls.query.paginate(page, 5, False)



class RentalModel(db.Model):
        __tablename__ = 'rentals'

        id = db.Column(db.Integer, primary_key=True)
        beg_date = db.Column(db.Date())
        end_date = db.Column(db.Date())
        price = db.Column(db.Float(precision=2))
        renter_name = db.Column(db.String(80))
        renter_mob_num = db.Column(db.String())

        parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'))
        parking = db.relationship('ParkingModel')

        def __init__(self, beg_date, price, renter_name,
                    renter_mob_num, parking_id):
            self.beg_date = beg_date
            self.end_date = None
            self.price = price
            self.renter_name = renter_name
            self.renter_mob_num = renter_mob_num
            self.parking_id = parking_id


        def json(self):
            return {'beg_date':self.beg_date, 'price':self.price,
                    'renter_name':self.renter_name,
                    'renter_mob_num':self.renter_mob_num}


        @classmethod
        def find_by_id(cls, id):
            return cls.query.filter_by(id=id).first()

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()
            print(self.__dict__)

        def update(self):
            object = RentalModel.query.filter_by(id=self.id).first()
            object.beg_date = self.beg_date
            object.renter_name = self.renter_name
            object.price = self.price
            object.renter_mob_num = self.renter_mob_num
            db.session.commit()


        def delete_from_db(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def rental_list(cls, page):
            return cls.query.paginate(page, 5, False)


        @classmethod
        def renters_list(cls):
            query = cls.query.all()
            return {'renters':[{'name':rental.renter_name,
                    'mob_num':rental.renter_mob_num} for rental in cls.query.all()]}

        @classmethod
        def list_of_active_rentals(cls, page):
            return cls.query.filter(cls.end_date==None).paginate(page, 5, False)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
