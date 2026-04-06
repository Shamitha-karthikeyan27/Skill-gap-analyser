"""
One-time script: creates and seeds the SQLite database.
Run once before starting app.py.
"""
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'skillgap.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT
);
CREATE TABLE IF NOT EXISTS job_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    description TEXT,
    icon TEXT DEFAULT '💼'
);
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES job_roles(id),
    skill_id INTEGER REFERENCES skills(id),
    required_level INTEGER DEFAULT 3,
    PRIMARY KEY (job_id, skill_id)
);
CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER REFERENCES users(id),
    skill_id INTEGER REFERENCES skills(id),
    PRIMARY KEY (user_id, skill_id)
);
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER REFERENCES skills(id),
    title TEXT NOT NULL,
    resource_url TEXT NOT NULL,
    resource_type TEXT DEFAULT 'Course',
    description TEXT
);
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    job_role_id INTEGER REFERENCES job_roles(id),
    location TEXT,
    apply_url TEXT,
    description TEXT
);
CREATE TABLE IF NOT EXISTS mock_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES job_roles(id),
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT
);
CREATE TABLE IF NOT EXISTS mock_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    job_id INTEGER REFERENCES job_roles(id),
    score INTEGER,
    total INTEGER,
    passed INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SKILLS = [
    ('Python','Programming'),('SQL','Database'),('Machine Learning','AI/ML'),
    ('Data Visualization','Analytics'),('Statistics','Analytics'),('Excel','Analytics'),
    ('Tableau','Visualization'),('Power BI','Visualization'),('React','Frontend'),
    ('JavaScript','Frontend'),('Node.js','Backend'),('HTML','Frontend'),('CSS','Frontend'),
    ('HTML/CSS','Frontend'),('MySQL','Database'),('Java','Programming'),('C','Programming'),
    ('C++','Programming'),('C#','Programming'),('Deep Learning','AI/ML'),('NLP','AI/ML'),
    ('Computer Vision','AI/ML'),('R Language','Analytics'),('Pandas','Data Science'),
    ('NumPy','Data Science'),('Scikit-learn','AI/ML'),('TensorFlow','AI/ML'),
    ('Communication','Soft Skills'),('MongoDB','Database'),('PostgreSQL','Database'),
    ('Docker','DevOps'),('Git','DevOps'),('Spring Boot','Backend'),('AWS','Cloud'),
    ('Azure','Cloud'),('GCP','Cloud'),('Jenkins','DevOps'),('Kubernetes','DevOps'),
    ('SAS','Analytics'),('MATLAB','Analytics'),('PyTorch','AI/ML'),('Keras','AI/ML'),
    ('Angular','Frontend'),('Vue.js','Frontend'),('Redis','Database'),
]

ROLES = [
    ('Data Analyst','Analyze data to uncover insights and drive business decisions using SQL, Excel, and visualization tools.','📊'),
    ('Data Scientist','Build predictive models and apply ML algorithms to solve complex real-world problems.','🧪'),
    ('Full Stack Developer','Develop complete web applications covering both frontend and backend systems.','💻'),
    ('Machine Learning Engineer','Design, build, and deploy ML models at scale in production environments.','🤖'),
    ('Business Analyst','Bridge business needs and technical solutions through data-driven analysis.','📈'),
]

ROLE_SKILLS = {
    'Data Analyst': ['Python','SQL','Statistics','Excel','Data Visualization','Tableau','Power BI'],
    'Data Scientist': ['Python','Machine Learning','Deep Learning','Statistics','Pandas','NumPy','Scikit-learn','TensorFlow','Inheritance','Class'],
    'Full Stack Developer': ['React','JavaScript','Node.js','HTML/CSS','SQL','MongoDB','Git','Class','Inheritance','Abstraction'],
    'Machine Learning Engineer': ['Python','Machine Learning','Deep Learning','TensorFlow','Docker','NLP','Computer Vision','Scikit-learn','Inheritance','Class'],
    'Business Analyst': ['SQL','Excel','Power BI','Statistics','Communication','Data Visualization'],
}

RECOMMENDATIONS = [
    ('Python','Python for Everybody (Coursera)','https://www.coursera.org/specializations/python','Course','Complete Python for beginners by University of Michigan.'),
    ('SQL','SQL for Data Science (Coursera)','https://www.coursera.org/learn/sql-for-data-science','Course','Learn SQL queries and data manipulation for analytics.'),
    ('Machine Learning','Machine Learning by Andrew Ng','https://www.coursera.org/learn/machine-learning','Course','The most popular ML course in the world.'),
    ('Tableau','Tableau Public Training','https://public.tableau.com/en-us/s/resources','Tutorial','Free official Tableau training resources.'),
    ('React','React Official Tutorial','https://react.dev/learn','Documentation','The official interactive React learning guide.'),
    ('Deep Learning','Deep Learning Specialization','https://www.coursera.org/specializations/deep-learning','Course','5-course deep learning specialization by Andrew Ng.'),
    ('Statistics','Statistics for Data Science','https://www.khanacademy.org/math/statistics-probability','Tutorial','Free stats & probability on Khan Academy.'),
    ('Power BI','Power BI Full Course','https://learn.microsoft.com/en-us/power-bi/','Documentation','Official Microsoft Power BI learning path.'),
    ('Pandas','Pandas Documentation','https://pandas.pydata.org/docs/','Documentation','Official Pandas docs with tutorials and guides.'),
    ('NumPy','NumPy Quickstart','https://numpy.org/doc/stable/user/quickstart.html','Documentation','Learn NumPy for scientific computing.'),
    ('Docker','Docker Getting Started','https://docs.docker.com/get-started/','Tutorial','Official Docker beginner guide.'),
    ('NLP','NLP with Python (NLTK Book)','https://www.nltk.org/book/','Tutorial','Free online book for NLP with Python.'),
    ('TensorFlow','TensorFlow Tutorials','https://www.tensorflow.org/tutorials','Documentation','Official TensorFlow tutorials for all levels.'),
    ('Git','Git & GitHub for Beginners','https://www.freecodecamp.org/news/git-and-github-for-beginners/','Tutorial','Beginner-friendly Git guide on freeCodeCamp.'),
    ('Excel','Excel Training (Microsoft)','https://support.microsoft.com/en-us/excel','Documentation','Free official Excel training by Microsoft.'),
    ('JavaScript','JavaScript.info','https://javascript.info/','Tutorial','The Modern JavaScript Tutorial — comprehensive and free.'),
    ('Node.js','Node.js Documentation','https://nodejs.org/en/docs/','Documentation','Official Node.js docs and guides.'),
    ('Scikit-learn','Scikit-learn User Guide','https://scikit-learn.org/stable/user_guide.html','Documentation','Official guide for ML with scikit-learn.'),
    ('HTML/CSS','HTML & CSS on freeCodeCamp','https://www.freecodecamp.org/learn/responsive-web-design/','Course','Free responsive web design certification.'),
    ('MongoDB','MongoDB University','https://learn.mongodb.com/','Course','Free official MongoDB courses and certifications.'),
]

COMPANIES = {
    'Data Analyst': [
        ('Google','Bengaluru, IN','https://careers.google.com','Google — Work on data-driven products at global scale.'),
        ('Amazon','Hyderabad, IN','https://www.amazon.jobs','Amazon — Data Analyst roles across AWS and retail.'),
        ('Flipkart','Bengaluru, IN','https://www.flipkartcareers.com','Data analyst openings in e-commerce analytics.'),
        ('Infosys','Pune, IN','https://www.infosys.com/careers','Business and data analytics consulting roles.'),
    ],
    'Data Scientist': [
        ('Microsoft','Hyderabad, IN','https://careers.microsoft.com','Data Scientist roles in Azure AI and cloud products.'),
        ('OpenAI','Remote','https://openai.com/careers','Research and applied science in cutting-edge AI.'),
        ('Razorpay','Bengaluru, IN','https://razorpay.com/jobs','Data Science roles in fintech.'),
    ],
    'Full Stack Developer': [
        ('Razorpay','Bengaluru, IN','https://razorpay.com/jobs','Full Stack roles in fintech product teams.'),
        ('Swiggy','Bengaluru, IN','https://careers.swiggy.com','Full Stack roles building India food-tech platform.'),
        ('Zoho','Chennai, IN','https://www.zoho.com/careers.html','Full Stack Developer at one of India top SaaS companies.'),
    ],
    'Machine Learning Engineer': [
        ('NVIDIA','Pune, IN','https://www.nvidia.com/en-us/about-nvidia/careers/','ML Engineer roles in GPU computing and AI infrastructure.'),
        ('Google DeepMind','London / Remote','https://deepmind.google/careers/','Cutting-edge ML research and engineering role.'),
        ('Samsung R&D','Bengaluru, IN','https://samsungrd.in/careers','ML engineering in consumer electronics and AI.'),
    ],
    'Business Analyst': [
        ('Wipro','Mumbai, IN','https://careers.wipro.com','Business Analyst roles in IT consulting.'),
        ('TCS','Pan India','https://www.tcs.com/careers','BA roles across industries and global clients.'),
        ('Accenture','Bengaluru, IN','https://www.accenture.com/in-en/careers','Strategy and analytics consulting BA roles.'),
    ],
}

MOCK_QUESTIONS = {
    'Data Analyst': [
        ('Which SQL clause filters grouped data?','WHERE','HAVING','GROUP BY','ORDER BY','B','HAVING filters groups; WHERE filters rows before grouping.'),
        ('What does a Box Plot show?','Distribution & outliers','Correlation','Time series','Category comparison','A','Box plots display median, quartiles, and outliers.'),
        ('Best Python library for data manipulation?','NumPy','Matplotlib','Pandas','Seaborn','C','Pandas is the primary library for data manipulation.'),
        ('Median of [3,7,9,2,5]?','3','5','7','9','B','Sorted: [2,3,5,7,9] → median = 5.'),
        ('Which is used for data cleaning?','Matplotlib','Seaborn','Pandas','Scikit-learn','C','Pandas has dropna(), fillna(), drop_duplicates().'),
        ('What does GROUP BY do in SQL?','Filters rows','Sorts results','Groups rows with same values','Joins tables','C','GROUP BY groups rows with matching values into summary rows.'),
        ('What is a NULL in SQL?','Zero value','Empty string','Missing/unknown value','False','C','NULL represents a missing or unknown value in a database.'),
        ('Which chart type shows proportions?','Bar chart','Line chart','Pie chart','Scatter plot','C','Pie charts effectively show part-to-whole relationships.'),
        ('What is standard deviation?','Average value','Middle value','Spread of data from mean','Most common value','C','Standard deviation measures how spread out data is.'),
        ('SQL command to get unique values?','UNIQUE','DISTINCT','DIFFERENT','FILTER','B','SELECT DISTINCT removes duplicate rows from results.'),
        ('What is a primary key?','A foreign key','Unique identifier for a row','A non-unique column','A type of chart','B','Primary keys uniquely identify each record in a table.'),
        ('What is data normalization?','Deleting redundant data','Grouping data by color','Formatting dates','None of above','A','Normalization reduces data redundancy and improves data integrity.'),
        ('Purpose of a JOIN in SQL?','Delete rows','Combine data from two tables','Sort data','Rename columns','B','JOINs are used to retrieve related data from multiple tables.'),
        ('What is a Histogram?','A type of pie chart','Graph showing frequency distribution','A time series line','None','B','Histograms show the distribution of numerical data.'),
        ('Which SQL command removes a table?','DELETE','REMOVE','DROP','CLEAR','C','DROP TABLE removes the entire table structure and data.'),
    ],
    'Data Scientist': [
        ('Best metric for imbalanced classification?','Accuracy','F1 Score','MSE','R-squared','B','F1 Score balances precision and recall for imbalanced data.'),
        ('What is overfitting?','Good train, poor test','Good test only','High bias','Low variance','A','Overfitting = memorized training data, fails to generalize.'),
        ('Algorithm for dimensionality reduction?','KNN','SVM','PCA','Random Forest','C','PCA reduces features while retaining variance.'),
        ('What is a train-test split?','Divides model into parts','Splits data for training vs evaluation','Runs two models','Filters data','B','Splits data so we can evaluate model on unseen data.'),
        ('What does p-value represent?','Model accuracy','Probability result by chance','Feature importance','Data size','B','A low p-value means the result is statistically significant.'),
        ('What is regularization?','Adding more data','Reducing model complexity to prevent overfitting','Increasing learning rate','Removing features','B','L1/L2 regularization penalizes large weights to reduce overfitting.'),
        ('Which is a supervised learning algorithm?','K-Means','PCA','Linear Regression','DBSCAN','C','Linear Regression learns from labeled data (supervised).'),
        ('What does the ROC curve plot?','Loss vs epochs','True vs False Positive Rate','Accuracy vs features','Precision vs F1','B','ROC plots TPR vs FPR to evaluate classification models.'),
        ('What is the bias-variance tradeoff?','Speed vs accuracy','Training time vs model size','Model error from assumptions vs sensitivity to data','None','C','High bias = underfitting, high variance = overfitting.'),
        ('Which library builds neural networks?','Pandas','Scikit-learn','TensorFlow','Matplotlib','C','TensorFlow (and PyTorch) are used to build neural networks.'),
        ('What is cross-validation?','Splits data once','Technique to evaluate model on multiple folds','A way to double data','None','B','K-fold cross-validation uses different parts of data for training/testing.'),
        ('What is a random forest?','A single tree','An ensemble of decision trees','A type of sorting','None','B','Random Forest uses multiple decision trees to improve accuracy.'),
        ('Purpose of an activation function?','Sort data','Introduce non-linearity into a neural network','Define model name','None','B','Activation functions allow neural networks to learn non-linear patterns.'),
        ('What is a learning rate?','Speed of model','Step size at each iteration while moving toward a minimum','Complexity of model','None','B','Learning rate controls how much to change the model in response to the error.'),
    ],
    'Full Stack Developer': [
        ('What does virtual DOM in React do?','Edits browser DOM directly','Computes optimal DOM updates','Stores user data','Renders server-side HTML','B','React diffs virtual DOM to apply minimal real DOM updates.'),
        ('HTTP method to update a resource?','GET','POST','PUT','DELETE','C','PUT replaces an existing resource; PATCH does partial updates.'),
        ('What is a REST API?','A database','A UI framework','An architectural style for web services','A testing tool','C','REST is a stateless client-server architectural style for APIs.'),
        ('What does async/await do in JS?','Makes code synchronous','Handles asynchronous operations cleanly','Speeds up code','Removes callbacks forever','B','async/await is syntactic sugar over Promises for async code.'),
        ('What does useState do in React?','Fetches data','Adds state to a functional component','Routes pages','Manages CSS','B','useState hook manages local state in a React component.'),
        ('What is a foreign key?','Primary identifier','Reference to another table primary key','Index on a column','Auto-generated number','B','Foreign keys enforce referential integrity between tables.'),
        ('Which runs JavaScript on the server?','React','Node.js','Angular','CSS','B','Node.js is a runtime that runs JavaScript outside the browser.'),
        ('What is CORS?','A CSS rule','A database term','Policy for cross-origin HTTP requests','A React hook','C','CORS controls which origins can access a web server.'),
        ('What does npm stand for?','Node Package Manager','New Program Module','None of above','Network Package Module','A','npm is the package manager for Node.js.'),
        ('What is Git used for?','Running a web server','Version control','Database management','UI styling','B','Git is a distributed version control system for code.'),
        ('Difference between == and === in JS?','No difference','=== checks type and value; == only value','== is faster','None','B','Strict equality (===) checks both value and data type.'),
        ('What is a CSS selector?','A way to find data','Pattern to select the elements you want to style','A JS library','None','B','Selectors are used to target HTML elements for styling.'),
        ('What is Redux?','A backend framework','State management for JS apps','A type of DB','None','B','Redux is often used with React to manage global app state.'),
        ('What does the "head" tag in HTML contain?','Main page content','Metadata and link to scripts/styles','Footer info','None','B','The head contains info NOT shown to the user, like titles and links.'),
    ],
    'Machine Learning Engineer': [
        ('What is a Docker container?','A virtual machine','Lightweight portable app environment','Database server','Cloud storage','B','Containers package app + dependencies into isolated environments.'),
        ('What does MLOps mean?','ML Operations — production deployment of ML models','ML Optimization','Manual Learning Operations','None','A','MLOps applies DevOps practices to ML model development and deployment.'),
        ('Purpose of a validation set?','Train the model','Test the final model','Tune hyperparameters','Store data','C','Validation set is used to tune hyperparameters during training.'),
        ('What is gradient descent?','A data structure','Optimization algorithm to minimize loss','A type of neural network','A regularization technique','B','Gradient descent iteratively updates params to minimize the loss function.'),
        ('What is model serialization?','Deleting a model','Saving a trained model to disk','Training on GPU','Data preprocessing','B','Serialization (e.g. pickle) saves a model for later use.'),
        ('What is an epoch in ML?','One pass through the whole training set','One pass through a single batch','The time it takes to train','Model score','A','An epoch is one complete pass through the entire training dataset.'),
        ('Which is a distance-based algorithm?','Linear Regression','Random Forest','KNN','Naive Bayes','C','K-Nearest Neighbors uses distance metrics like Euclidean distance.'),
        ('What is the "kernel trick" in SVM?','A ways to use GPUs','Mapping data to higher dimensions without computing them','Removing outliers','A data cleaning method','B','The kernel trick allows SVMs to find non-linear boundaries in high-dim space.'),
        ('What is transfer learning?','Moving data between servers','Using a pre-trained model on a new task','Changing model parameters','Training from scratch','B','Transfer learning uses knowledge from a pre-trained model for a related task.'),
        ('Common library for MLOps tracking?','NumPy','MLflow','Pandas','Requests','B','MLflow is widely used for experiment tracking and model management.'),
        ('What is a feature vector?','A matrix','Numerical representation of object features','A model type','None','B','Feature vectors represent various attributes of an object in a numerical way.'),
        ('What is hyperparameter tuning?','Training the model','Finding the best params for a model','Cleaning data','None','B','Tuning involves selecting the best set of hyperparameters for an algorithm.'),
        ('What is a confusion matrix?','A complex DB','Table used to evaluate classification performance','A data error','None','B','A confusion matrix shows True/False Positives/Negatives.'),
        ('What is "Inference" in ML?','Training the model','Using a trained model to make predictions','Writing code','None','B','Inference is the process of using a deployed model on new data.'),
    ],
    'Business Analyst': [
        ('What is a KPI?','Key Performance Indicator','Key Process Index','Know Progress Item','None','A','KPIs are measurable values showing how well objectives are being achieved.'),
        ('What is a BRD?','Business Requirements Document','Binary Result Data','Basic Reporting Document','None','A','A BRD formally captures the business solution for a project.'),
        ('What does SWOT stand for?','Strengths, Weaknesses, Opportunities, Threats','Software, Work, Operation, Test','None','Skills, Work, Options, Tasks','A','SWOT analysis evaluates internal and external business factors.'),
        ('What is a stakeholder?','A database table','A person with interest in the project','A type of chart','An SQL command','B','Stakeholders are individuals or groups affected by or interested in the project.'),
        ('What is meant by data-driven decision making?','Using gut feeling','Making decisions based on data analysis','Guessing outcomes','Avoiding data','B','Data-driven decisions use facts and analytics rather than assumptions.'),
        ('What does "Scope Creep" mean?','Uncontrolled changes in a project scope','A type of virus','A project manager personality','Meeting deadlines early','A','Scope creep is when a project grows beyond its original goal without approval.'),
        ('What is a User Story?','A biography of a user','Short description of a feature from user perspective','A marketing ad','A technical manual','B','User stories explain what a user wants and why, in simple terms.'),
        ('Which tool is best for Business Intelligence dashboards?','Notepad','Excel','Tableau','Photoshop','C','Tableau (and Power BI) are dedicated BI tools for data visualization.'),
        ('What is requirement elicitation?','Deleting requirements','Gathering requirements from stakeholders','Testing the app','Marketing the product','B','Elicitation is the process of discovering requirements from users.'),
        ('What does MVP stand for?','Most Valuable Player','Minimum Viable Product','Maximum Value project','None','B','MVP is a product with just enough features to satisfy early customers.'),
        ('What is a Gantt chart?','A pie chart','Timeline for project management','A flow chart','None','B','Gantt charts visualize project schedules and task sequences.'),
        ('What is requirement prioritization?','Deleting requirements','Ordering requirements by importance/risk','Writing more code','None','B','Prioritization ensures the most critical features are built first.'),
        ('What is a Use Case?','A test plan','Description of how a user interacts with a system','A bug report','None','B','Use cases capture specific interactions between characters and systems.'),
        ('What is User Acceptance Testing (UAT)?','Testing by developers','Final phase where real users test the system','A performance test','None','B','UAT verifies if the system meets business requirements before launch.'),
    ],
}


def seed():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()

    # Skills
    conn.executemany("INSERT OR IGNORE INTO skills (name, category) VALUES (?,?)", SKILLS)
    conn.commit()

    # Roles
    conn.executemany("INSERT OR IGNORE INTO job_roles (title, description, icon) VALUES (?,?,?)", ROLES)
    conn.commit()

    # Role → Skill mapping
    for role_title, skill_names in ROLE_SKILLS.items():
        role = conn.execute("SELECT id FROM job_roles WHERE title=?", (role_title,)).fetchone()
        if not role: continue
        for sname in skill_names:
            skill = conn.execute("SELECT id FROM skills WHERE name=?", (sname,)).fetchone()
            if skill:
                conn.execute("INSERT OR IGNORE INTO job_skills (job_id, skill_id) VALUES (?,?)", (role['id'], skill['id']))
    conn.commit()

    # Recommendations
    for (sname, title, url, rtype, desc) in RECOMMENDATIONS:
        skill = conn.execute("SELECT id FROM skills WHERE name=?", (sname,)).fetchone()
        if skill:
            conn.execute("INSERT OR IGNORE INTO recommendations (skill_id,title,resource_url,resource_type,description) VALUES (?,?,?,?,?)",
                         (skill['id'], title, url, rtype, desc))
    conn.commit()

    # Companies
    for role_title, cos in COMPANIES.items():
        role = conn.execute("SELECT id FROM job_roles WHERE title=?", (role_title,)).fetchone()
        if not role: continue
        for (name, loc, url, desc) in cos:
            conn.execute("INSERT OR IGNORE INTO companies (name,job_role_id,location,apply_url,description) VALUES (?,?,?,?,?)",
                         (name, role['id'], loc, url, desc))
    conn.commit()

    # Mock questions
    for role_title, questions in MOCK_QUESTIONS.items():
        role = conn.execute("SELECT id FROM job_roles WHERE title=?", (role_title,)).fetchone()
        if not role: continue
        for q in questions:
            conn.execute("""INSERT OR IGNORE INTO mock_questions
                (job_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation)
                VALUES (?,?,?,?,?,?,?,?)""", (role['id'],) + q)
    conn.commit()
    conn.close()
    print("✅ Database seeded successfully at:", DB)

if __name__ == '__main__':
    seed()
