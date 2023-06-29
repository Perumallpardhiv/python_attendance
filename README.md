# Virtual Attendance using Python

This attendance system utilizes facial recognition to verify the presence of students in the database. Upon scanning a student's face, it checks if their details are already registered. If present, their name and the time of attendance are recorded in a .csv file. In case the student is not found in the database, their photo is taken with their consent and stored for future attendance records.

To prevent attendance fraud, a solution has been implemented wherein attendance is tracked only when the left eye is blinked, effectively mitigating any attempts to bypass the system by presenting a photo.
