import MySQLdb
import traceback

host = "localhost"
user = "root"
password = "123456"
db = "matrix"

db_conn = MySQLdb.connect(host = host,
                        user = user,
                        passwd = password,
                        db = db)

cursor = db_conn.cursor()

'''
Get configuration of a problem from database

@Param prob_id
    problem id

@return problem configure
    in string
'''
def get_problem_config(prob_id):
    cursor.execute("\
    select config from library_problem \
    where prob_id = %d"  % (prob_id,))

    return cursor.fetchone()[0]

'''
Set grade of a submission

@Param sub_id
    The submission id
@Param grade
    grade value

@return
    no return value
'''
def set_grade(sub_id, grade):
    try:
        cursor.execute("\
        update submission \
        set grade = %d \
        where sub_id = %d" % (grade, sub_id))
        db_conn.commit()
    except MySQLdb.Error as e:
        db_conn.rollback()
        raise e

'''
Get waiting submissions' id

@return
    A list contains dicts with sub_id and prob_id, where
    sub_id is the submission's id and
    prob_id is the corresponding problem's id
'''
def get_waiting_id():
    cursor.execute("\
    select sub_id, prob_id from submission \
    where grade is NULL")
    return [{"sub_id": grade[0], "prob_id": grade[1]}
            for grade in cursor.fetchall()]


def set_submission_report(sub_id, report):
    try:
        cursor.execute("\
        update submission \
        set report = %s \
        where sub_id = %s", (report, sub_id))
        db_conn.commit()
    except MySQLdb.Error as e:
        db_conn.rollback()
        raise e
