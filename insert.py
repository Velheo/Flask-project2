from app import db, Wine, Sort, Producer

if __name__=='__main__':
    db.create_all()

    koblevo = Producer(name='Koblevo')
    massandra = Producer(name='Massandra')
    vardiani = Producer(name='Vardiani')

    rd = Sort(name='red dry')
    rsd = Sort(name='red semi-dry')
    wd = Sort(name='white dry')
    rsw = Sort(name='red sweet')

    wines = [
        Wine(name='Cabernet', price=45.00, producer=koblevo, sort=rd, top=1),
        Wine(name='Marlo', price=50.00, producer=massandra, sort=rsd, top=1),
        Wine(name='Aligothe', price=40.00, producer=massandra, sort=wd),
        Wine(name='Portwein', price=65.00, producer=koblevo, sort=rsw),
        Wine(name='Hwanchkara', price=90.00, producer=vardiani, sort=rsd, top=1),
        Wine(name='Cagor', price=55.00, producer=massandra, sort=rsw),
        Wine(name='Saperavi', price=75.00, producer=vardiani, sort=rd),
        Wine(name='Cabernet', price=50.00, producer=massandra, sort=rd),
        Wine(name='Chardonet', price=65.00, producer=koblevo, sort=wd),
    ]

    items = [koblevo, massandra, vardiani, rd, rsd, wd, rsw] + wines
    db.session.add_all(items)
    db.session.commit()