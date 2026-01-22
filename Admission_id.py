def generate_admission_id(branch, year, cursor):
    year_short = str(year)[-2:]

    cursor.execute("""
        SELECT admission_id FROM student_admission
        WHERE branch=%s AND admission_year=%s
        ORDER BY admission_id DESC LIMIT 1
    """, (branch, year))

    last = cursor.fetchone()

    if last:
        last_num = int(last[0][-3:]) + 1
    else:
        last_num = 1

    return f"{branch}{year_short}{str(last_num).zfill(3)}"
