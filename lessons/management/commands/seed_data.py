from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lessons.models import Course, Lesson


class Command(BaseCommand):
    help = 'Seeds the database with sample courses and lessons'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Get or create a default instructor
        instructor, created = User.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@ctrlshift.academy',
                'is_staff': True,
                'is_active': True
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS('Created instructor user'))

        # Course 1: Introduction to Python
        course1, created = Course.objects.get_or_create(
            title='Introduction to Python Programming',
            defaults={
                'description': 'Learn the fundamentals of Python programming from scratch. This comprehensive course covers variables, data types, control structures, functions, and more. Perfect for beginners with no prior programming experience.',
                'instructor': instructor,
                'is_published': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course1.title}'))

            # Lessons for Course 1
            lessons_data = [
                {
                    'title': 'Getting Started with Python',
                    'content': 'Welcome to Python programming! In this lesson, you will learn about Python, its history, and why it\'s one of the most popular programming languages today.\n\nPython is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum and first released in 1991, Python emphasizes code readability and allows programmers to express concepts in fewer lines of code.\n\nKey Features of Python:\n- Easy to learn and read\n- Large standard library\n- Cross-platform compatibility\n- Strong community support\n- Versatile for web development, data science, automation, and more\n\nIn the next lessons, we\'ll dive into hands-on programming!',
                    'order': 1
                },
                {
                    'title': 'Variables and Data Types',
                    'content': 'In this lesson, you\'ll learn about variables and the different data types in Python.\n\nVariables:\nVariables are containers for storing data values. In Python, you don\'t need to declare the type of a variable.\n\nExample:\nname = "John"\nage = 25\nheight = 5.9\nis_student = True\n\nData Types:\n1. Strings (str) - Text data: "Hello World"\n2. Integers (int) - Whole numbers: 42\n3. Floats (float) - Decimal numbers: 3.14\n4. Booleans (bool) - True or False\n5. Lists - Ordered collections: [1, 2, 3]\n6. Dictionaries - Key-value pairs: {"name": "John", "age": 25}\n\nPractice creating variables with different data types!',
                    'order': 2
                },
                {
                    'title': 'Control Flow - If Statements',
                    'content': 'Control flow statements allow you to control the execution of your code based on certain conditions.\n\nIf Statements:\nIf statements execute code only when a condition is True.\n\nSyntax:\nif condition:\n    # code to execute\nelif another_condition:\n    # code to execute\nelse:\n    # code to execute\n\nExample:\nage = 18\n\nif age >= 18:\n    print("You are an adult")\nelif age >= 13:\n    print("You are a teenager")\nelse:\n    print("You are a child")\n\nComparison Operators:\n- == (equal to)\n- != (not equal to)\n- > (greater than)\n- < (less than)\n- >= (greater than or equal to)\n- <= (less than or equal to)\n\nTry writing your own if statements!',
                    'order': 3
                },
                {
                    'title': 'Loops in Python',
                    'content': 'Loops allow you to repeat code multiple times, making your programs more efficient.\n\nFor Loops:\nUsed to iterate over a sequence (list, tuple, string, etc.)\n\nExample:\nfor i in range(5):\n    print(i)\n# Prints: 0, 1, 2, 3, 4\n\nfruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(fruit)\n\nWhile Loops:\nExecute code as long as a condition is True.\n\nExample:\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n\nLoop Control:\n- break: Exit the loop\n- continue: Skip to next iteration\n- pass: Do nothing (placeholder)\n\nPractice writing loops to automate repetitive tasks!',
                    'order': 4
                },
                {
                    'title': 'Functions in Python',
                    'content': 'Functions are reusable blocks of code that perform specific tasks. They help organize code and avoid repetition.\n\nDefining Functions:\ndef function_name(parameters):\n    # code to execute\n    return result\n\nExample:\ndef greet(name):\n    return f"Hello, {name}!"\n\nmessage = greet("Alice")\nprint(message)  # Output: Hello, Alice!\n\nFunction Parameters:\n- Required parameters\n- Default parameters: def greet(name="Guest")\n- Keyword arguments: greet(name="Bob")\n- Variable-length arguments: *args, **kwargs\n\nReturn Values:\nFunctions can return values using the return statement.\n\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)\nprint(result)  # Output: 8\n\nBest Practices:\n- Use descriptive function names\n- Keep functions focused on a single task\n- Document your functions with docstrings\n\nStart creating your own functions!',
                    'order': 5
                }
            ]

            for lesson_data in lessons_data:
                Lesson.objects.create(course=course1, **lesson_data)
                self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson_data["title"]}'))

        # Course 2: Web Development Basics
        course2, created = Course.objects.get_or_create(
            title='Web Development Fundamentals',
            defaults={
                'description': 'Master the fundamentals of web development including HTML, CSS, and JavaScript. Learn to build responsive, modern websites from scratch. This course is perfect for aspiring web developers.',
                'instructor': instructor,
                'is_published': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course2.title}'))

            lessons_data = [
                {
                    'title': 'Introduction to HTML',
                    'content': 'HTML (HyperText Markup Language) is the standard markup language for creating web pages.\n\nBasic Structure:\n<!DOCTYPE html>\n<html>\n  <head>\n    <title>Page Title</title>\n  </head>\n  <body>\n    <h1>My First Heading</h1>\n    <p>My first paragraph.</p>\n  </body>\n</html>\n\nCommon HTML Tags:\n- <h1> to <h6>: Headings\n- <p>: Paragraphs\n- <a>: Links\n- <img>: Images\n- <div>: Container\n- <ul>, <ol>, <li>: Lists\n- <form>, <input>: Forms\n\nHTML provides the structure and content of web pages. In the next lessons, we\'ll learn how to style them with CSS!',
                    'order': 1
                },
                {
                    'title': 'CSS Styling Basics',
                    'content': 'CSS (Cascading Style Sheets) is used to style and layout web pages.\n\nCSS Syntax:\nselector {\n  property: value;\n}\n\nExample:\nh1 {\n  color: blue;\n  font-size: 24px;\n}\n\nThree Ways to Add CSS:\n1. Inline: <h1 style="color:blue;">Heading</h1>\n2. Internal: <style> tag in <head>\n3. External: Link to .css file\n\nCommon CSS Properties:\n- color: Text color\n- background-color: Background color\n- font-size: Text size\n- margin: Space outside element\n- padding: Space inside element\n- border: Element border\n- display: Layout type\n- width, height: Dimensions\n\nCSS Selectors:\n- Element: h1\n- Class: .my-class\n- ID: #my-id\n- Attribute: [type="text"]\n\nStart styling your web pages!',
                    'order': 2
                },
                {
                    'title': 'JavaScript Fundamentals',
                    'content': 'JavaScript is a programming language that enables interactive web pages.\n\nVariables:\nlet name = "John";\nconst age = 25;\nvar oldWay = "deprecated";\n\nFunctions:\nfunction greet(name) {\n  return `Hello, ${name}!`;\n}\n\nconst greet = (name) => `Hello, ${name}!`;\n\nDOM Manipulation:\n// Select elements\nconst element = document.querySelector(\'.my-class\');\nconst elements = document.querySelectorAll(\'p\');\n\n// Modify content\nelement.textContent = "New text";\nelement.innerHTML = "<strong>Bold text</strong>";\n\n// Add event listeners\nelement.addEventListener(\'click\', function() {\n  alert(\'Clicked!\');\n});\n\nCommon Events:\n- click: Mouse click\n- submit: Form submission\n- keyup: Key released\n- load: Page loaded\n\nJavaScript brings your web pages to life!',
                    'order': 3
                }
            ]

            for lesson_data in lessons_data:
                Lesson.objects.create(course=course2, **lesson_data)
                self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson_data["title"]}'))

        # Course 3: Database Design
        course3, created = Course.objects.get_or_create(
            title='Database Design and SQL',
            defaults={
                'description': 'Learn how to design efficient databases and write powerful SQL queries. Understand relational database concepts, normalization, and optimization techniques. Essential for backend developers and data professionals.',
                'instructor': instructor,
                'is_published': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course3.title}'))

            lessons_data = [
                {
                    'title': 'Introduction to Databases',
                    'content': 'A database is an organized collection of structured data stored electronically.\n\nTypes of Databases:\n1. Relational (SQL): MySQL, PostgreSQL, SQLite\n2. NoSQL: MongoDB, Redis, Cassandra\n3. Graph: Neo4j\n4. Document: Couchbase\n\nRelational Database Concepts:\n- Tables: Store data in rows and columns\n- Rows: Individual records\n- Columns: Attributes or fields\n- Primary Key: Unique identifier\n- Foreign Key: Links tables together\n\nWhy Use Databases?\n- Organized data storage\n- Fast data retrieval\n- Data integrity\n- Concurrent access\n- Security features\n\nRelational databases use SQL (Structured Query Language) to interact with data. In the next lessons, we\'ll learn SQL!',
                    'order': 1
                },
                {
                    'title': 'SQL Basics - SELECT Queries',
                    'content': 'SQL (Structured Query Language) is used to communicate with databases.\n\nSELECT Statement:\nRetrieve data from tables.\n\nBasic Syntax:\nSELECT column1, column2\nFROM table_name;\n\nSelect All Columns:\nSELECT * FROM users;\n\nWHERE Clause:\nFilter results based on conditions.\n\nSELECT * FROM users\nWHERE age > 18;\n\nORDER BY:\nSort results.\n\nSELECT * FROM users\nORDER BY name ASC;\n\nLIMIT:\nRestrict number of results.\n\nSELECT * FROM users\nLIMIT 10;\n\nCommon Operators:\n- =, !=, >, <, >=, <=\n- AND, OR, NOT\n- LIKE: Pattern matching\n- IN: Match multiple values\n- BETWEEN: Range\n\nExample:\nSELECT name, email\nFROM users\nWHERE age BETWEEN 18 AND 65\nAND city = \'New York\'\nORDER BY name;\n\nPractice writing SELECT queries!',
                    'order': 2
                }
            ]

            for lesson_data in lessons_data:
                Lesson.objects.create(course=course2, **lesson_data)
                self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson_data["title"]}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total courses created: {Course.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total lessons created: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nInstructor credentials:'))
        self.stdout.write(self.style.SUCCESS('  Username: instructor'))
        self.stdout.write(self.style.SUCCESS('  Password: instructor123'))
