count_break_time_for_day_range = "select date, sum((strftime('%s', end_break_time) - strftime('%s', start_break_time))/60) as minutes from break where employee_id = {employee_id} and date between '{start_date}' and '{end_date}' group by date"

count_attendance_time_for_day_range = "select date, sum((strftime('%s', out_time) - strftime('%s', in_time))/60) as minutes, in_time, out_time from attendance where employee_id = {employee_id} and date between '{start_date}' and '{end_date}' group by date"