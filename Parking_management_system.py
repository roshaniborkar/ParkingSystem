import mysql.connector 
import time
from datetime import date


global conn,cursor
conn = mysql.connector.connect(
    host='localhost', database=' parking_system_new', user='root', password='rose')
cursor = conn.cursor()


def clear():
  for _ in range(1):
     print()

def made_by():
    msg = ''' 
            Parking Management system made by           : ROSHANI R BORKAR
            USN                                         : 1NH21CS414
            College                                     : NEW HORIZON COLLEGE OF ENGINEERING
            year                                        : 2022-23
            
            Thanks for evaluating my Project.
            \n\n\n
        '''

    for x in msg:
        print(x, end='')
        time.sleep(0.002)

    wait = input('Press any key to continue.....')

def display_parking_type_records():
    cursor.execute('select * from parking_type;')
    records = cursor.fetchall()
    for row in records:
        print(row)

def login():
    while True:
        clear()
        uname = input('Enter your id :')
        upass = input('Enter your Password :')
        cursor.execute('select * from login where name="{}" and pwd ="{}"'.format(uname,upass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows!=1:
            print('Invalid Login details..... Try again')
        else:
            print('You are eligible for operating this system............')
            print('\n\n\n')
            break


def add_parking_type_record():
    clear()
    name = input('Enter Parking Type( 1. Two wheelar 2. Car 3. Bus 4. Truck 5. Trolly ) : ')
    price =  input('Enter Parking Price per day : ')
    sql = 'insert into parking_type(name,price) values("{}",{});'.format(name,price)
    cursor.execute(sql)
    print('\n\n New Parking Type added....')
    cursor.execute('select max(id) from parking_type')
    no = cursor.fetchone()
    print(' New Parking Type ID is : {} \n\n\n'.format(no[0]))
    wait= input('\n\n\nPress any key to continue............')


def modify_parking_type_record():
    clear()
    print(' M O D I F Y   P A R K I N G   T Y P E  S C R E E N ')
    print('-'*100)
    print('1.  Parking Type Name \n')
    print('2.  Parking Price  \n')
    choice = int(input('Enter your choice :'))
    field=''
    if choice==1:
        field='name'
    if choice==2:
        field='price'
    
    park_id = input('Enter Parking Type ID :')
    value = input('Enter new values :')
    sql = 'update parking_type set '+ field +' = "' + value +'" where id ='+ park_id +';'
    cursor.execute(sql)
    print('Record updated successfully................')
    display_parking_type_records()
    wait = input('\n\n\nPress any key to continue............')


def add_new_vehicle():
    clear()
    print('ＶＥＨＩＣＬＥ ＬＯＧＩＮ ＳＣＲＥＥＮ')
    print('-'*100)
    vehicle_id = input('Enter Vehicle Number :' )
    print('\n parking Id is 1->Bike,2->Car,3->bus,4->Truck,5->trolly')
    parking_id = input('Enter parking ID (vehicle type):')
    entry_date = date.today()
    sql = 'insert into transaction(vehicle_id,parking_id,entry_date) values \
           ("{}","{}","{}");'.format(vehicle_id,parking_id,entry_date)
    cursor.execute(sql)
    cursor.execute('update parking_space set status ="full" where id ={}'.format(parking_id))
    print('\n\n\n Record added successfully.................')
    wait= input('\n\n\nPress any key to continue.....')


def remove_vehicle():
    clear()
    print('ＶＥＨＩＣＬＥ ＬＯＧＯＵＴ ＳＣＲＥＥＮ')
    print('-'*100)
    vehicle_id = input('Enter vehicle No :')
    exit_date = date.today()
    sql = 'select parking_id,price,entry_date from transaction tr,parking_space ps, parking_type pt \
           where tr.parking_id = ps.id and ps.type_id = pt.id and \
           vehicle_id ="'+vehicle_id+'" and exit_date is NULL;'
    cursor.execute(sql)
    record = cursor.fetchone()
    days = (exit_date-record[2]).days 
    if days ==0:
        days = days+1
    amount = record[1]*days
    clear()
    print('Logout Details ')
    print('-'*100)
    print('Parking ID : {}'.format(record[0]))
    print('Vehicle ID : {}'.format(vehicle_id))
    print('Parking Date : {}'.format(record[2]))
    print('Current Date : {}'.format(exit_date))
    print('Amount Payable : {}'.format(amount))
    wait = input('press any key to continue......')
    sql1 = 'update transaction set exit_date ="{}" , amount ={} where vehicle_id ="{}" \
            and exit_date is NULL;'.format(exit_date,amount, vehicle_id)
    sql2 =  'update parking_space set status ="open" where id = {}'.format(record[0])
    cursor.execute(sql1)
    cursor.execute(sql2)
    wait = input('Vehicle Out from our System Successfully.......\n Press any key to continue....')


def search_menu():
    clear()
    print(' S E A R C H  P A R K I N G  M E N U ')
    print('1.  Parking ID (1->Bike,2->Car,3->bus,4->Truck,5->trolly)\n')
    print('2.  Vehicle Parked  \n')

    choice = int(input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'id'
    if choice == 2:
        field = 'vehicle No'
    if choice == 3:
        field = 'status'
    value = input('Enter value to search :')
    if choice == 1 or choice==3:
        print('\nt_id,v_type,ammount,status')
        sql = 'select ps.id,name,price, status \
          from parking_space ps , parking_type pt where ps.id = pt.id AND ps.id ={}'.format(value)
    else:
        print('\nv_id, vehicle_no,v_id, entry date')
        sql = 'select id,vehicle_id,parking_id,entry_date from transaction where exit_date is NULL;'

    cursor.execute(sql)
    results = cursor.fetchall()
    records = cursor.rowcount
    for row in results:
        print(row)
    if records < 1:
        print('Record not found \n\n\n ')
    wait = input('\n\n\nPress any key to continue......')


def parking_status(status):
    clear()
    print('Parking Status :',status)
    print('-'*100)
    print('slot,vehicle,availablity')
    print('no   type')
    sql ="select * from parking_space where status ='{}'".format(status)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait =input('\n\n\nPress any key to continue.....')

def vehicle_status_report():
    clear()
    print('Vehicle Status - Currently Parked')
    print('-'*100)
    sql='select * from transaction where exit_date is NULL;'
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait =input('\n\n\nPress any key to continue.....')

def money_collected():
    clear()
    start_date = input('Enter start Date(yyyy-mm-dd): ')
    end_date = input('Enter End Date(yyyy-mm-dd): ')
    sql = "select sum(amount) from transaction where \
          entry_date ='{}' and exit_date ='{}'".format(start_date,end_date)
    cursor.execute(sql)
    result = cursor.fetchone()
    clear()
    print('Total money Collected from {} to {}'.format(start_date,end_date))
    print('-'*100)
    print(result[0])
    wait =input('\n\n\nPress any key to continue.....')


def report_menu():
    while True:
        clear()
        print(' P A R K I N G    R E P O R T S  ')
        print('-'*100)
        print('1.  Parking Types \n')
        print('2.  Free Space  \n')
        print('3.  Ocupied Space  \n')
        print('4.  Vehicle Status  \n')
        print('5.  Money Collected  \n')
        print('6.  Exit  \n')
        choice = int(input('Enter your choice :'))
        field = ''
        if choice == 1:
            display_parking_type_records()
        if choice == 2:
            parking_status("open")
        if choice == 3:
            parking_status("full")
        if choice == 4:
            vehicle_status_report()
        if choice == 5:
            money_collected()
        if choice ==6: 
            break
        



def main_menu():
    clear()
    login()
  
    
    while True:
      clear()
      print(' P A R K I N G   M A N A G E M E N T    S Y S T E M')
      print('*'*100)
      print("\n1.  Vehicle Login ")
      print('\n2.  Vehicle Logout')
      print('\n3.  Add New Parking Type')
      print('\n4.  Modify Parking Type Record')
      print('\n5.  Search menu')
      print('\n6.  Report menu')
      print('\n7.  Close application')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))

      if choice == 1:
        add_new_vehicle()

      if choice == 2:
        remove_vehicle()

      if choice == 3:
        add_parking_type_record()
      
      if choice == 4:
        modify_parking_type_record()

      if choice == 5:
        search_menu()
      
      if choice == 6:
        report_menu()

      if choice == 7:
        break
        
    made_by()


if __name__ == "__main__":
    main_menu()
