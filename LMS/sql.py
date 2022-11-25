import pymysql
from sshtunnel import SSHTunnelForwarder
import pandas as pd

# create table consulting_list
# (
# 	  id INT NOT NULL auto_increment,
#     student_id int NOT NULL,
#     student_register_id varchar(10),
#     student_name varchar(30) NOT NULL,
#     student_phone varchar(30) NOT NULL,
# 	  parents_id INT NOT NULL,
#     parents_name varchar(30) NOT NULL,
#     parents_phone varchar(30) NOT NULL,
#     parents_email varchar(100) default "",
#     teacher_id INT NOT NULL,
#     teacher_name varchar(30) NOT NULL,
#     ban_id INT NOT NULL,
#     ban_name varchar(30) NOT NULL,
#     documents_code INT NOT NULL,
#     documents_content text NOT NULL,
#     documents_time datetime NOT NULL,
#     etc varcharacter(50),
#     attempt int NOT NULL default 0,
#     PRIMARY KEY (id)
# );
#
# alter table consulting_list auto_increment=10000;


# create table teacher_todo_list
# (
# 	  id INT NOT NULL auto_increment,
#     teacher_id int NOT NULL,
#     teacher_name varchar(30) NOT NULL,
#     ban_id int NOT NULL,
#     ban_name varchar(30),
#     category int NOT NULL,
#     isend int NOT NULL,
#     content text NOT NULL,
#     start_time datetime NOT NULL,
#     end_time datetime NOT NULL,
#     etc varchar(100),
#     PRIMARY KEY (id)
# );
#
# alter table teacher_todo_list auto_increment=1;


def ssh_db_tunneling_select(class_name, types):
    with SSHTunnelForwarder(
        ('15.164.36.206'),
        ssh_username="ec2-user",
        ssh_pkey="D:/purple_academy_privkey.pem",
        remote_bind_address=('purple-lms-mariadb-1.cdpnol1tlujr.ap-northeast-2.rds.amazonaws.com', 3306)
    ) as tunnel:
        print("=== SSH Tunnel ===")

        db = pymysql.connect(
            host='127.0.0.1', user="readonly",
            password="purpledbreadonly12!@", port=tunnel.local_bind_port, database='purple-lms'
        )
        try:
            with db.cursor() as cur:
                if types == 'student':
                    # ['id', 'register_no', 'main_class_id', 'admission_date', 'first_name', 'last_name', 'nick_name', 'gender', 'birthday', 'religion', 'caste', 'blood_group', 'mother_tongue', 'current_address', 'permanent_address', 'city', 'state', 'mobileno', 'category_id', 'email', 'parent_id', 'route_id', 'vehicle_id', 'hostel_id', 'room_id', 'previous_details', 'photo', 'ar', 'chambit', 'lexile', 'myon', 'reading_week', 'created_at', 'updated_at', 'badge_type', 'badge_type_date', 'badge_reset_date', 'del_yn']
                    cur.execute(f'select * from student A where A.main_class_id IN (select B.id from class B where B.name = "{class_name}");')
                    rows = cur.fetchall()
                    cur.execute(f'SHOW columns FROM student;')
                    cols = cur.fetchall()

                elif types == 'teacher':
                    # ['id', 'staff_id', 'name', 'name_kor', 'department', 'qualification', 'experience_details', 'total_experience', 'designation', 'joining_date', 'birthday', 'sex', 'religion', 'blood_group', 'present_address', 'permanent_address', 'mobileno', 'email', 'salary_template_id', 'branch_id', 'photo', 'facebook_url', 'linkedin_url', 'twitter_url', 'created_at', 'updated_at', 'price_1', 'price_2', 'price_3', 'price_4', 'price_5', 'price_6', 'price_7', 'price_8', 'price_9', 'price_10', 'price_11', 'price_12', 'price_13', 'price_14', 'price_15', 'price_16', 'price_17', 'price_18', 'price_19', 'price_20', 'price_21', 'price_22']
                    cur.execute(f'select * from staff C where C.id IN (select teacher_id from teacher_allocation A where A.class_id IN (select B.id from class B where B.name = "{class_name}"));')
                    rows = cur.fetchall()
                    cur.execute(f'SHOW columns FROM staff;')
                    cols = cur.fetchall()

                elif types == 'parents':
                    # [A.id, A.register_no, A.first_name as 학생이름, A.email, B.name, B.email, B.mobileno]
                    cur.execute(f'select A.id, A.register_no, A.first_name as 학생이름, A.email, B.name, B.email, B.mobileno from student A join parent B on (A.parent_id = B.id and A.main_class_id in (select C.id from class C where C.name = "{class_name}"));')
                    # cur.execute(f'select * from student A join parent B on (A.parent_id = B.id and A.main_class_id in (select C.id from class C where C.name = "{class_name}"));')
                    rows = cur.fetchall()
                    cur.execute(f'SHOW columns FROM staff;')
                    cols = cur.fetchall()

                row_list = []
                for i in rows:
                    row_list.append(list(i))

                col_list = []
                for i in cols:
                    col_list.append(i[0])

                data_list = []
                for i in row_list:
                    data_list.append({name: value for name, value in zip(col_list, i)}.copy())
        except:
            print("fail")
        finally:
            db.close()
            return data_list


def ssh_db_tunneling_select_class():
    with SSHTunnelForwarder(
        ('15.164.36.206'),
        ssh_username="ec2-user",
        ssh_pkey="D:/purple_academy_privkey.pem",
        remote_bind_address=('purple-lms-mariadb-1.cdpnol1tlujr.ap-northeast-2.rds.amazonaws.com', 3306)
    ) as tunnel:
        print("=== SSH Tunnel ===")

        db = pymysql.connect(
            host='127.0.0.1', user="readonly",
            password="purpledbreadonly12!@", port=tunnel.local_bind_port, database='purple-lms'
        )
        try:
            with db.cursor() as cur:
                # ['id', 'class_type', 'section_id', 'subject_id', 'is_regular', 'name', 'week_auto', 'week', 'start_date', 'end_date', 'name_numeric', 'created_at', 'updated_at', 'branch_id', 'schedule_file_name', 'schedule_enc_name', 'timetable_id', 'is_ended', 'rewriting_class']
                cur.execute(f'SELECT * FROM class;;')
                rows = cur.fetchall()
                cur.execute(f'SHOW columns FROM class;')
                cols = cur.fetchall()

                row_list = []
                for i in rows:
                    row_list.append(list(i))

                col_list = []
                for i in cols:
                    col_list.append(i[0])

                data_list = []
                for i in row_list:
                    data_list.append({name: value for name, value in zip(col_list, i)}.copy())


        except:
            print("fail")
        finally:
            db.close()
            return data_list


def ssh_db_tunneling_select_student():
    with SSHTunnelForwarder(
        ('15.164.36.206'),
        ssh_username="ec2-user",
        ssh_pkey="D:/purple_academy_privkey.pem",
        remote_bind_address=('purple-lms-mariadb-1.cdpnol1tlujr.ap-northeast-2.rds.amazonaws.com', 3306)
    ) as tunnel:
        print("=== SSH Tunnel ===")

        db = pymysql.connect(
            host='127.0.0.1', user="readonly",
            password="purpledbreadonly12!@", port=tunnel.local_bind_port, database='purple-lms'
        )
        try:
            with db.cursor() as cur:
                # ['id', 'class_type', 'section_id', 'subject_id', 'is_regular', 'name', 'week_auto', 'week', 'start_date', 'end_date', 'name_numeric', 'created_at', 'updated_at', 'branch_id', 'schedule_file_name', 'schedule_enc_name', 'timetable_id', 'is_ended', 'rewriting_class']
                cur.execute(f'SELECT * FROM student;;')
                rows = cur.fetchall()
                cur.execute(f'SHOW columns FROM student;')
                cols = cur.fetchall()

                row_list = []
                for i in rows:
                    row_list.append(list(i))

                col_list = []
                for i in cols:
                    col_list.append(i[0])

                data_list = []
                for i in row_list:
                    data_list.append({name: value for name, value in zip(col_list, i)}.copy())
        except:
            print("fail")
        finally:
            db.close()
            return data_list


def select_consulting(class_name):
    # database 확인
    # ssh tunneling
    # 반 이름으로 상담 목록 가져오기

    db = pymysql.connect(
        host='127.0.0.1', user="root",
        password="1q2w3e4r", port=3306, database='consulting'
    )
    try:
        with db.cursor() as cur:
            cur.execute(
                    f'select * from consulting_list where ban_name = "{class_name}";')
            rows = cur.fetchall()

            cur.execute(
                f'SHOW columns FROM consulting_list;')
            cols = cur.fetchall()

            row_list = []
            for i in rows:
                row_list.append(list(i))

            col_list = []
            for i in cols:
                col_list.append(i[0])

            data_list = []
            for i in row_list:
                data_list.append({name: value for name, value in zip(col_list, i)}.copy())
    except:
        print("fail")
    finally:
        db.close()
        return data_list


def insert_consulting(data):
    # database 확인
    # consulting_list 테이블
    # attempt는 insert할 때 기존에 있던 값에 +1
    # UPDATE consulting_list SET attempt=(기존 attempt + 1) WHERE id="";
    # data type은 tuple(tuple)
    # (
    #         (1, "P111111", "test_student_name", "010-1111-1111", 1, "test_parents_name", "010-2222-2222",
    #          "test_parents_email", 1, "test_teacher_name", 1, "teas_ban_name", 0, "test_content", "etc", 1),
    #     )
    # id는 10000부터 시작해서 1씩 자동으로 증가

    sql = "insert into consulting_list(student_id, student_register_id, student_name, student_phone, parents_id, parents_name, parents_phone, parents_email, teacher_id, teacher_name, ban_id, ban_name, documents_code, documents_content, documents_time, etc, attempt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s);"

    db = pymysql.connect(
        host='127.0.0.1', user="root",
        password="1q2w3e4r", port=3306, database='consulting'
    )
    try:
        with db.cursor() as cur:
            if len(data) == 0:
                pass
            elif len(data) == 1:
                cur.execute(sql, data[0])
            else:
                cur.executemany(sql, data)
            db.commit()
        print(200)
    except:
        print("fail")

    finally:
        db.close()


def select_todo_list(class_name):
    # database 확인
    # ssh tunneling
    # 반 이름으로 상담 리스트 select

    db = pymysql.connect(
        host='127.0.0.1', user="root",
        password="1q2w3e4r", port=3306, database='consulting'
    )
    try:
        with db.cursor() as cur:
            cur.execute(f'select * from teacher_todo_list where ban_name = "{class_name}";')
            rows = cur.fetchall()

            cur.execute(
                f'SHOW columns FROM consulting_list;')
            cols = cur.fetchall()

            row_list = []
            for i in rows:
                row_list.append(list(i))

            col_list = []
            for i in cols:
                col_list.append(i[0])

            data_list = []
            for i in row_list:
                data_list.append({name: value for name, value in zip(col_list, i)}.copy())
    except:
        print("fail")
    finally:
        db.close()
        return data_list


# a, b = ssh_db_tunneling_select('Pluto Plus B1', 'teacher')
# a = ssh_db_tunneling_select_class()
# a, b = ssh_db_tunneling_select_student()
a = ssh_db_tunneling_select('Pluto Plus B1', 'student')
# ssh_db_tunneling_select('Pluto Plus B1', 'parents')
# select_todo_list("ban1")
# select_consulting("test_ban_name")
# insert_consulting((
#         (2, "P111112", "test_student_name", "010-1111-1111", 1, "test_parents_name", "010-2222-2222",
#          "test_parents_email", 1, "test_teacher_name", 1, "test_ban_name", 0, "test_content", "etc", 1),
#         (2, "P111112", "test_student_name", "010-1111-1111", 1, "test_parents_name", "010-2222-2222",
#          "test_parents_email", 1, "test_teacher_name", 1, "test_ban_name", 0, "test_content", "etc", 1),
#     ))
# for i in a:
#     print(i['id'])
#     print(i['register_no'])
