-- ============================================================
-- Smart Skill Gap Analyzer — Full Database Schema
-- ============================================================

-- USERS
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SKILLS MASTER LIST
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);

-- JOB ROLES
CREATE TABLE IF NOT EXISTS job_roles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(10) DEFAULT '💼'
);

-- SKILLS REQUIRED PER ROLE
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES job_roles(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    required_level INTEGER DEFAULT 3,
    PRIMARY KEY (job_id, skill_id)
);

-- USER UPLOADED RESUME SKILLS
CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, skill_id)
);

-- GAP ANALYSIS RESULTS
CREATE TABLE IF NOT EXISTS gap_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES job_roles(id) ON DELETE CASCADE,
    overall_score FLOAT,
    matched_skills TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LEARNING RECOMMENDATIONS
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    skill_id INTEGER REFERENCES skills(id),
    title VARCHAR(200) NOT NULL,
    resource_url TEXT NOT NULL,
    resource_type VARCHAR(50) DEFAULT 'Course',
    description TEXT
);

-- COMPANIES
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    job_role_id INTEGER REFERENCES job_roles(id) ON DELETE CASCADE,
    location VARCHAR(100),
    apply_url TEXT,
    description TEXT
);

-- MOCK TEST QUESTIONS (options stored as comma-separated)
CREATE TABLE IF NOT EXISTS mock_questions (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES job_roles(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,  -- 'A','B','C','D'
    explanation TEXT
);

-- MOCK TEST RESULTS
CREATE TABLE IF NOT EXISTS mock_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES job_roles(id),
    score INTEGER,
    total INTEGER,
    passed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SEED DATA
-- ============================================================

-- Skills
INSERT INTO skills (name, category) VALUES
('Python', 'Programming'),
('SQL', 'Database'),
('Machine Learning', 'AI/ML'),
('Data Visualization', 'Analytics'),
('Statistics', 'Analytics'),
('Excel', 'Analytics'),
('Tableau', 'Visualization'),
('Power BI', 'Visualization'),
('React', 'Frontend'),
('JavaScript', 'Frontend'),
('Node.js', 'Backend'),
('HTML/CSS', 'Frontend'),
('Deep Learning', 'AI/ML'),
('NLP', 'AI/ML'),
('Computer Vision', 'AI/ML'),
('R Language', 'Analytics'),
('Pandas', 'Data Science'),
('NumPy', 'Data Science'),
('Scikit-learn', 'AI/ML'),
('TensorFlow', 'AI/ML'),
('Communication', 'Soft Skills'),
('MongoDB', 'Database'),
('PostgreSQL', 'Database'),
('Docker', 'DevOps'),
('Git', 'DevOps')
ON CONFLICT (name) DO NOTHING;

-- Job Roles
INSERT INTO job_roles (title, description, icon) VALUES
('Data Analyst', 'Analyze data to uncover insights and drive business decisions using SQL, Excel, and visualization tools.', '📊'),
('Data Scientist', 'Build predictive models and apply ML algorithms to solve complex real-world problems.', '🧪'),
('Full Stack Developer', 'Develop complete web applications covering both frontend and backend systems.', '💻'),
('Machine Learning Engineer', 'Design, build, and deploy ML models at scale in production environments.', '🤖'),
('Business Analyst', 'Bridge business needs and technical solutions through data-driven analysis.', '📈')
ON CONFLICT (title) DO NOTHING;

-- Role → Required Skills mapping
-- Data Analyst (id=1): Python, SQL, Statistics, Excel, Data Vis, Tableau, Power BI
INSERT INTO job_skills (job_id, skill_id) SELECT jr.id, s.id FROM job_roles jr, skills s 
WHERE jr.title='Data Analyst' AND s.name IN ('Python','SQL','Statistics','Excel','Data Visualization','Tableau','Power BI')
ON CONFLICT DO NOTHING;

-- Data Scientist (id=2): Python, ML, Deep Learning, Statistics, Pandas, NumPy, Scikit-learn
INSERT INTO job_skills (job_id, skill_id) SELECT jr.id, s.id FROM job_roles jr, skills s
WHERE jr.title='Data Scientist' AND s.name IN ('Python','Machine Learning','Deep Learning','Statistics','Pandas','NumPy','Scikit-learn','TensorFlow')
ON CONFLICT DO NOTHING;

-- Full Stack Developer (id=3): React, JavaScript, Node.js, HTML/CSS, SQL, MongoDB, Git
INSERT INTO job_skills (job_id, skill_id) SELECT jr.id, s.id FROM job_roles jr, skills s
WHERE jr.title='Full Stack Developer' AND s.name IN ('React','JavaScript','Node.js','HTML/CSS','SQL','MongoDB','Git')
ON CONFLICT DO NOTHING;

-- ML Engineer (id=4): Python, ML, Deep Learning, TensorFlow, Docker, NLP, Computer Vision
INSERT INTO job_skills (job_id, skill_id) SELECT jr.id, s.id FROM job_roles jr, skills s
WHERE jr.title='Machine Learning Engineer' AND s.name IN ('Python','Machine Learning','Deep Learning','TensorFlow','Docker','NLP','Computer Vision','Scikit-learn')
ON CONFLICT DO NOTHING;

-- Business Analyst (id=5): SQL, Excel, Power BI, Statistics, Communication
INSERT INTO job_skills (job_id, skill_id) SELECT jr.id, s.id FROM job_roles jr, skills s
WHERE jr.title='Business Analyst' AND s.name IN ('SQL','Excel','Power BI','Statistics','Communication','Data Visualization')
ON CONFLICT DO NOTHING;

-- Recommendations
INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Python for Everybody (Coursera)', 'https://www.coursera.org/specializations/python', 'Course', 'Comprehensive Python for beginners by University of Michigan.'
FROM skills s WHERE s.name='Python' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'SQL for Data Science (Coursera)', 'https://www.coursera.org/learn/sql-for-data-science', 'Course', 'Learn SQL queries and data manipulation for analytics.'
FROM skills s WHERE s.name='SQL' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Machine Learning by Andrew Ng', 'https://www.coursera.org/learn/machine-learning', 'Course', 'The most popular ML course in the world. Highly recommended.'
FROM skills s WHERE s.name='Machine Learning' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Tableau Public Training', 'https://public.tableau.com/en-us/s/resources', 'Tutorial', 'Free official Tableau training resources and datasets.'
FROM skills s WHERE s.name='Tableau' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'React Official Tutorial', 'https://react.dev/learn', 'Documentation', 'The official interactive React learning guide.'
FROM skills s WHERE s.name='React' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Deep Learning Specialization', 'https://www.coursera.org/specializations/deep-learning', 'Course', '5-course deep learning specialization by Andrew Ng.'
FROM skills s WHERE s.name='Deep Learning' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Statistics for Data Science', 'https://www.khanacademy.org/math/statistics-probability', 'Tutorial', 'Free statistics & probability course on Khan Academy.'
FROM skills s WHERE s.name='Statistics' ON CONFLICT DO NOTHING;

INSERT INTO recommendations (skill_id, title, resource_url, resource_type, description)
SELECT s.id, 'Power BI Full Course', 'https://learn.microsoft.com/en-us/power-bi/', 'Documentation', 'Official Microsoft Power BI learning path.'
FROM skills s WHERE s.name='Power BI' ON CONFLICT DO NOTHING;

-- Companies
INSERT INTO companies (name, job_role_id, location, apply_url, description)
SELECT jr.id, jr.id, 'Bengaluru, IN', 'https://careers.google.com', 'Google — Work on data-driven products at global scale.'
FROM job_roles jr WHERE jr.title='Data Analyst' ON CONFLICT DO NOTHING;

INSERT INTO companies (name, job_role_id, location, apply_url, description) VALUES
('Amazon', (SELECT id FROM job_roles WHERE title='Data Analyst'), 'Hyderabad, IN', 'https://www.amazon.jobs', 'Amazon — Data Analyst roles across AWS and retail divisions.'),
('Flipkart', (SELECT id FROM job_roles WHERE title='Data Analyst'), 'Bengaluru, IN', 'https://www.flipkartcareers.com', 'Data analyst openings in e-commerce analytics.'),
('Infosys', (SELECT id FROM job_roles WHERE title='Data Analyst'), 'Pune, IN', 'https://www.infosys.com/careers', 'Business and data analytics consulting roles.'),
('Microsoft', (SELECT id FROM job_roles WHERE title='Data Scientist'), 'Hyderabad, IN', 'https://careers.microsoft.com', 'Data Scientist roles in Azure AI and cloud products.'),
('OpenAI', (SELECT id FROM job_roles WHERE title='Data Scientist'), 'Remote', 'https://openai.com/careers', 'Research and applied science in cutting-edge AI.'),
('Razorpay', (SELECT id FROM job_roles WHERE title='Full Stack Developer'), 'Bengaluru, IN', 'https://razorpay.com/jobs', 'Full Stack Developer roles in fintech product teams.'),
('Swiggy', (SELECT id FROM job_roles WHERE title='Full Stack Developer'), 'Bengaluru, IN', 'https://careers.swiggy.com', 'Full Stack roles building India food-tech platform.'),
('NVIDIA', (SELECT id FROM job_roles WHERE title='Machine Learning Engineer'), 'Pune, IN', 'https://www.nvidia.com/en-us/about-nvidia/careers/', 'ML Engineer roles in GPU computing and AI infrastructure.'),
('Wipro', (SELECT id FROM job_roles WHERE title='Business Analyst'), 'Mumbai, IN', 'https://careers.wipro.com', 'Business Analyst roles in IT consulting and transformation.')
ON CONFLICT DO NOTHING;

-- Mock Questions — Data Analyst
INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which SQL clause is used to filter grouped data?',
  'WHERE', 'HAVING', 'GROUP BY', 'ORDER BY', 'B',
  'HAVING filters groups created by GROUP BY, whereas WHERE filters rows before grouping.'
FROM job_roles jr WHERE jr.title='Data Analyst';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'What does a Box Plot primarily show?',
  'Distribution & outliers', 'Correlation', 'Time series trend', 'Category comparison', 'A',
  'Box plots display median, quartiles, and outliers — great for data distribution analysis.'
FROM job_roles jr WHERE jr.title='Data Analyst';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which Python library is best for data manipulation?',
  'NumPy', 'Matplotlib', 'Pandas', 'Seaborn', 'C',
  'Pandas is the primary library for data manipulation and analysis in Python.'
FROM job_roles jr WHERE jr.title='Data Analyst';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'What is the median of [3, 7, 9, 2, 5]?',
  '3', '5', '7', '9', 'B',
  'Sorted array is [2,3,5,7,9], so median is the middle value = 5.'
FROM job_roles jr WHERE jr.title='Data Analyst';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which of the following is used for data cleaning?',
  'Matplotlib', 'Seaborn', 'Pandas', 'Scikit-learn', 'C',
  'Pandas provides functions like dropna(), fillna(), drop_duplicates() for data cleaning.'
FROM job_roles jr WHERE jr.title='Data Analyst';

-- Mock Questions — Data Scientist
INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which metric is best for imbalanced classification datasets?',
  'Accuracy', 'F1 Score', 'Mean Squared Error', 'R-squared', 'B',
  'F1 Score balances precision and recall, making it suitable for imbalanced datasets.'
FROM job_roles jr WHERE jr.title='Data Scientist';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'What does "overfitting" mean in Machine Learning?',
  'Model performs well on train, poorly on test', 'Model performs well on test only', 'Model has high bias', 'None of above', 'A',
  'Overfitting means the model has memorized training data but fails to generalize.'
FROM job_roles jr WHERE jr.title='Data Scientist';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which algorithm is used for dimensionality reduction?',
  'KNN', 'SVM', 'PCA', 'Random Forest', 'C',
  'Principal Component Analysis (PCA) reduces the number of features while retaining variance.'
FROM job_roles jr WHERE jr.title='Data Scientist';

-- Mock Questions — Full Stack Developer
INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'What does "virtual DOM" in React do?',
  'Directly edits browser DOM', 'Computes optimal DOM updates', 'Stores user data', 'Renders HTML server-side', 'B',
  'React virtual DOM diffs changes and applies only the minimum required updates to the real DOM.'
FROM job_roles jr WHERE jr.title='Full Stack Developer';

INSERT INTO mock_questions (job_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
SELECT jr.id,
  'Which HTTP method is used to update an existing resource?',
  'GET', 'POST', 'PUT', 'DELETE', 'C',
  'PUT replaces an existing resource. PATCH does partial updates.'
FROM job_roles jr WHERE jr.title='Full Stack Developer';
