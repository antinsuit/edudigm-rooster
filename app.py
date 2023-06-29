from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
  return render_template('home.html')


@app.route('/run_script', methods=['POST'])
def run_script():
  import pandas as pd
  from itertools import permutations
  gsheetid = "1_DjJlN-HQjwquJD4WNvjf6-5l2X3F6KNwEkO9VJdewU"
  sheet_name = "teacher_details"
  teacher_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(
    gsheetid, sheet_name)
  teacher_preferences = pd.read_csv(teacher_url).fillna('_')
  teachers_monday = {}
  teachers_tuesday = {}
  teachers_wednesday = {}
  teachers_thrusday = {}
  teachers_friday = {}
  teachers_saturday = {}
  teachers_sunday = {}
  days = [
    'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday',
    'sunday'
  ]
  teachers_days = {
    'monday': teachers_monday,
    'tuesday': teachers_tuesday,
    'wednesday': teachers_wednesday,
    'thrusday': teachers_thrusday,
    'friday': teachers_friday,
    'saturday': teachers_saturday,
    'sunday': teachers_sunday
  }

  for day in teachers_days.keys():
    teachers = teachers_days[day]
    for i, row in teacher_preferences.iterrows():
      if (row['available on ' + day] == 'yes'):
        teacher_id = row['teacher_ID']
        contact = row['contact details']
        main_subjects = [x.strip() for x in row['main subjects'].split(',')]
        backup_subjects = [
          x.strip() for x in row['backup subjects'].split(',')
        ]
        main_centers = [x.strip() for x in row['main_centers'].split(',')]
        backup_centers = [x.strip() for x in row['backup_centers'].split(',')]
        alloted_center = '_'
        count = 0
        teachers[teacher_id] = {
          'count':count,
          'contact': contact,
          'main subjects': main_subjects,
          'backup subjects': backup_subjects,
          'main centers': main_centers,
          'backup centers': backup_centers,
          'alloted center': alloted_center,
          'slots': []
        }
        teachers_days[day] = teachers

  def fill_schedule(COE, schedule, day, teachers_days):
    contacts = []
    teachers = {}
    teachers_alloted = []
    teachers = teachers_days[day]
    # Iterate through the school schedule and assign classes to teachers
    for index, row in schedule.iterrows():
      Timing = row['Timings']
      cells = [x for x in row[2:len(row) + 1]]
      subjects = []
      for x in cells:
        if (x.strip() == 'Break'):
          break
        elif (x.strip() == '_'):
          subjects.append(x)
        else:
          '''x=Class 3: M Aratrika'''
          subjects.append(
            x.split(' ')[1][0:len(x.split(' ')[1]) - 1] + x.split(' ')[2])
      #Iterate through the subject in parallel
      for subject in subjects:
        if (subject != '_'):
          alloted = 0
          # Iterate through the teachers in their preference order
          for teacher_id in teachers.keys():
            teacher = teachers[teacher_id]
            # Check if the teacher can teach the subject and center
            if (((teacher['alloted center'] == '_') and
                 (COE in teacher['main centers']))
                or (teacher['alloted center'] == COE)):
              if ((subject in teacher['main subjects'])
                  and (Timing in teacher['slots'] or teacher['slots'] == [])):
                if teacher['alloted center'] == '_':
                  teacher['alloted center'] = COE
                  try:
                    contacts.append(teacher_id + ' : ' + teacher['contact'])
                    teachers_alloted.append(teacher_id)
                  except:
                    print(teacher['contact'])
                  teacher['slots'] = [x for x in schedule['Timings']]
                  flag = COE
                written = ' '.join(cells[subjects.index(subject)].split(' ')
                                   [0:3]) + ' ' + teacher_id
                schedule.iloc[index, subjects.index(subject) + 2] = written
                teacher['count']+=1 
                teacher['slots'].remove(Timing)
                alloted = 1
                break
          if (alloted != 1):
            for teacher_id in teachers.keys():
              teacher = teachers[teacher_id]
              # Check if the teacher can teach the subject and center
              if (((teacher['alloted center'] == '_') and
                   (COE in teacher['main centers']))
                  or (teacher['alloted center'] == COE)):
                if ((subject in teacher['backup subjects']) and
                    (Timing in teacher['slots'] or teacher['slots'] == [])):
                  if teacher['alloted center'] == '_':
                    teacher['alloted center'] = COE
                    teacher['slots'] = [x for x in schedule['Timings']]
                    contacts.append(teacher_id + ' : ' + teacher['contact'])
                    teachers_alloted.append(teacher_id)
                  written = ' '.join(cells[subjects.index(subject)].split(' ')
                                     [0:3]) + ' ' + teacher_id
                  schedule.iloc[index, subjects.index(subject) + 2] = written
                  teacher['slots'].remove(Timing)
                  teacher['count']+=1 
                  alloted = 1
                  break
          if (alloted != 1):
            for teacher_id in teachers.keys():
              teacher = teachers[teacher_id]
              if (((teacher['alloted center'] == '_') and
                   (COE in teacher['backup centers']))
                  or (teacher['alloted center'] == COE)):
                if ((subject in teacher['main subjects']) and
                    (Timing in teacher['slots'] or teacher['slots'] == [])):
                  if teacher['alloted center'] == '_':
                    teacher['alloted center'] = COE
                    teacher['slots'] = [x for x in schedule['Timings']]
                    contacts.append(teacher_id + ' : ' + teacher['contact'])
                    teachers_alloted.append(teacher_id)
                  written = ' '.join(cells[subjects.index(subject)].split(' ')
                                     [0:3]) + ' ' + teacher_id
                  schedule.iloc[index, subjects.index(subject) + 2] = written
                  teacher['slots'].remove(Timing)
                  teacher['count']+=1 
                  alloted = 1
                  break
          if (alloted != 1):
            for teacher_id in teachers.keys():
              teacher = teachers[teacher_id]
              if (((teacher['alloted center'] == '_') and
                   (COE in teacher['backup centers']))
                  or (teacher['alloted center'] == COE)):
                if ((subject in teacher['backup subjects']) and
                    (Timing in teacher['slots'] or teacher['slots'] == [])):
                  if teacher['alloted center'] == '_':
                    teacher['alloted center'] = COE
                    teacher['slots'] = [x for x in schedule['Timings']]
                    contacts.append(teacher_id + ' : ' + teacher['contact'])
                    teachers_alloted.append(teacher_id)
                  written = ' '.join(cells[subjects.index(subject)].split(' ')
                                     [0:3]) + ' ' + teacher_id
                  schedule.iloc[index, subjects.index(subject) + 2] = written
                  teacher['slots'].remove(Timing)
                  teacher['count']+=1 
                  alloted = 1
                  break
          if (alloted != 1):
            written = ' '.join(cells[subjects.index(subject)].split(' ')
                               [0:3]) + ' ' + "not alloted"
            schedule.iloc[index, subjects.index(subject) + 2] = written
            alloted = 1
    new_contacts = []
    for i in range(len(contacts)):
        dic = teachers[teachers_alloted[i]]
        st = contacts[i] + ", slots:" + str(dic['count'])
        new_contacts.append(st)
    teachers_days[day] = teachers
    return new_contacts

  sheet_name = "COE_list"
  sheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(
    gsheetid, sheet_name)
  COE_list = pd.read_csv(sheet_url).fillna('_')
  tables = []
  table_heading = []
  for index, row in COE_list.iterrows():
    COE = row[0].strip()
    for day in row[1:]:
      if day in days:
        schedule_sheet_name = COE + '_' + day
        schedule_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(
          gsheetid, schedule_sheet_name)
        schedule = pd.read_csv(schedule_url).fillna('_')
        contact = fill_schedule(COE, schedule, day, teachers_days)
        missing_values = [' '] * (len(schedule) - len(contact))
        contact = contact + missing_values
        schedule['contact details'] = contact
        tables.append(schedule)
        table_heading.append(schedule_sheet_name)

  # Pass the list of DataFrames to the HTML template
  return render_template('result.html',
                         tables=tables,
                         table_heading=table_heading)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
