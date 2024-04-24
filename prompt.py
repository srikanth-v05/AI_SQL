from langchain_core.prompts.prompt import PromptTemplate

template1 =  """You work normal chatbot and also Given below are the table structures in the analytics database raw schema in SQL database: 
depart (Department_id int, Department_Name text);its department table details 
student_query (Student_id int, Student_Name text,Year text,CGPA double,Department_Id int); its student table details 
teacher (Teacher_Id int,Teacher_Name text,Department_Id text );

if year is taken provide output in roman

dont use like %  when you use department names 

consider the department names as below:
    Artificial Intelligence and Data Science or AI & DS or aids or ai&ds or AI&DS
    Information Technology or IT or it
    Computer Science Engineering or cse ir CSE
    Electronics and Communication Engineering or ECE or ece

Take user questions and respond back with SQL queries.

Take user question question as normal conversation and give respons for this question , but not make that normal one as sql query 
    let us user give hi , you say hi how can i assist you other wise you work with sql query

    
Example: 


User question: display the table
Your generated SQL query:
SELECT * FROM Department_Information;

User question: Get the names of all departments along with the total number of students and teachers in each department.
Your generated SQL query:
SELECT d.Department_Name, COUNT(DISTINCT s.Student_id) AS Total_Students, COUNT(DISTINCT t.Teacher_Id) AS Total_Teachers 
FROM depart d 
LEFT JOIN student_query s ON d.Department_id = .Department_Id 
LEFT JOIN teacher t ON d.Department_id = t.Department_Id 
GROUP BY d.Department_Name;

User question: display the second year students of department 2
Your generated SQL query:
SELECT s.Student_id, s.Student_Name
FROM student_query s
JOIN depart d ON s.Department_Id = d.Department_id
WHERE s.Year = II AND d.Department_id = 2;

User question: display the  students of Information technology  
Your generated SQL query:
SELECT s.Student_id, s.Student_Name, s.Year, s.CGPA, d.Department_Name
FROM student_query s
JOIN depart d ON s.Department_Id = d.Department_id
WHERE d.Department_Name = 'Information Technology';

User question: display the  students of IT or It or it
Your generated SQL query:
SELECT s.Student_id, s.Student_Name, s.Year, s.CGPA, d.Department_Name
FROM student_query s
JOIN depart d ON s.Department_Id = d.Department_id
WHERE d.Department_Name = 'Information Technology';

  
User question: {input}
Your generated SQL query: """

ENTITY_MEMORY_CONVERSATION_TEMPLATE = PromptTemplate(
    input_variables=["input"],
    template=template1,
)



_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE = """Given below are the table structures in the analytics database raw schema in SQL database: 
depart (Department_id int, Department_Name text);its department table details 
student_query (Student_id int, Student_Name text,Year text,CGPA double,Department_Id int); its student table details 
teacher (Teacher_Id int,Teacher_Name text,Department_Id text );


if year is taken provide output in roman


dont use like %  when you use department names

consider the department names as below:
    Artificial Intelligence and Data Science or AI & DS or aids or ai&ds or AI&DS
    Information Technology or IT or it
    Computer Science Engineering or cse ir CSE
    Electronics and Communication Engineering or ECE or ece

Take user questions and respond back with SQL queries.;

Take user question question as normal conversation and give respons for this question , but not make that normal one as sql query 
    let us user give hi , you say hi how can i assist you other wise you work with sql query

EXAMPLE

Conversation history:
Person #1: Please show me the departments table.
AI: SELECT * FROM Department_Information
Last line:
Person #1: Show me the students names whose cgpa is above 9 where department id is 3.
Output: SELECT s.Student_Name
FROM student_query s
WHERE s.CGPA > 9
AND s.Department_Id = 3;
Person #1: display the second year students of department 3
Output:SELECT s.Student_id, s.Student_Name
FROM student_query s
JOIN depart d ON s.Department_Id = d.Department_id
WHERE s.Year = 'II' AND d.Department_id = 3;

END OF EXAMPLE


Conversation history (for reference only):
{history}
Last line of conversation (for extraction):
User: {input}

Context:
{entities}

Current conversation:
{history}
Last line:
Human: {input}
You:"""


ENTITY_MEMORY_CONVERSATION_TEMPLATE1 = PromptTemplate(
    input_variables=["entities", "history","input"],
    template=_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE,
)


