"""
Static, in-memory course/skill catalogue for the Course Recommendation agent.

This catalogue is pure knowledge - it contains NO recommendation logic.
It exists to be serialized and sent to the LLM as grounding data so the
model itself can decide, per-student, which courses are relevant, which
skill gaps genuinely exist, how to order a learning path, and why. Python
code in this module only stores and retrieves Course records; it never
maps a career goal to a fixed list of courses.

Public interface (kept stable so callers do not need to change):
    Course
    CATALOGUE
    get_course(course_id)
    get_all_courses()
"""
from dataclasses import dataclass, field


@dataclass
class Course:
    id: str
    name: str
    description: str
    category: str
    difficulty: str  # "Beginner" | "Intermediate" | "Advanced"
    prerequisites: list[str] = field(default_factory=list)  # course ids
    duration: str = ""
    skills_gained: list[str] = field(default_factory=list)

    # Additional grounding metadata for the LLM. All optional/additive -
    # existing code that only reads the original fields keeps working.
    career_roles: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    related_skills: list[str] = field(default_factory=list)
    optional_tools: list[str] = field(default_factory=list)
    learning_outcomes: list[str] = field(default_factory=list)


CATALOGUE: list[Course] = [
    # ============================================================
    # PROGRAMMING FUNDAMENTALS
    # ============================================================
    Course(
        id="python",
        name="Python Programming",
        description=(
            "Core Python syntax and semantics: variables, control flow, functions, "
            "object-oriented programming, exception handling, file I/O, and virtual "
            "environments, applied through small practical programs."
        ),
        category="Programming Fundamentals",
        difficulty="Beginner",
        prerequisites=[],
        duration="3-4 weeks",
        skills_gained=[
            "Python", "Functions", "Object-Oriented Programming",
            "Exception Handling", "File Handling", "Virtual Environments",
        ],
        career_roles=[
            "Software Developer", "Backend Developer", "Python Developer",
            "Data Analyst", "Data Scientist", "Automation Engineer",
            "QA Engineer", "DevOps Engineer",
        ],
        keywords=["python", "scripting", "general-purpose programming"],
        related_skills=["Data Structures", "Algorithms"],
        optional_tools=["pip", "venv", "VS Code"],
        learning_outcomes=[
            "Write and structure Python scripts and modules",
            "Model data with classes and objects",
            "Handle errors and file input/output safely",
        ],
    ),
    Course(
        id="java",
        name="Java Programming",
        description=(
            "Statically-typed, object-oriented programming with Java: classes, "
            "interfaces, collections, generics, and exception handling, with an "
            "emphasis on building maintainable enterprise-style applications."
        ),
        category="Programming Fundamentals",
        difficulty="Beginner",
        prerequisites=[],
        duration="4-5 weeks",
        skills_gained=[
            "Java", "Object-Oriented Programming", "Collections Framework",
            "Generics", "Exception Handling", "JVM Basics",
        ],
        career_roles=[
            "Software Developer", "Java Developer", "Application Developer",
            "Backend Developer", "Android Developer",
        ],
        keywords=["java", "jvm", "object-oriented"],
        related_skills=["Design Patterns", "Multithreading"],
        optional_tools=["IntelliJ IDEA", "Maven", "Gradle"],
        learning_outcomes=[
            "Design classes and interfaces following OOP principles",
            "Use Java's collections framework effectively",
            "Build and package a runnable Java application",
        ],
    ),
    Course(
        id="csharp",
        name="C# Programming",
        description=(
            "Object-oriented programming in C# for the .NET platform, covering "
            "types, LINQ, async/await, and the .NET class library fundamentals "
            "needed to build desktop, web, and service applications."
        ),
        category="Programming Fundamentals",
        difficulty="Beginner",
        prerequisites=[],
        duration="3-4 weeks",
        skills_gained=["C#", "Object-Oriented Programming", "LINQ", "Async/Await", ".NET Basics"],
        career_roles=[".NET Developer", "Software Developer", "Application Developer", "Backend Developer"],
        keywords=["c#", "dotnet", "microsoft stack"],
        related_skills=["Design Patterns"],
        optional_tools=["Visual Studio", "NuGet"],
        learning_outcomes=[
            "Write idiomatic, type-safe C# code",
            "Use LINQ to query in-memory and external data",
            "Understand asynchronous programming with async/await",
        ],
    ),
    Course(
        id="cpp",
        name="C++ Programming",
        description=(
            "Systems-level programming with C++: memory management, pointers, "
            "the standard template library, and performance-conscious code, as a "
            "foundation for embedded, game, and high-performance systems work."
        ),
        category="Programming Fundamentals",
        difficulty="Intermediate",
        prerequisites=[],
        duration="5-6 weeks",
        skills_gained=["C++", "Pointers & Memory Management", "STL", "Performance Optimization Basics"],
        career_roles=[
            "Software Engineer", "Embedded Systems Engineer", "Game Developer",
            "Robotics Software Engineer", "Systems Engineer",
        ],
        keywords=["c++", "systems programming", "performance"],
        related_skills=["Data Structures", "Algorithms"],
        optional_tools=["CMake", "GDB", "Visual Studio"],
        learning_outcomes=[
            "Manage memory manually and understand pointer semantics",
            "Use the C++ Standard Template Library",
            "Write and debug performance-sensitive code",
        ],
    ),
    Course(
        id="git_version_control",
        name="Git & Version Control",
        description=(
            "Track code changes, branch and merge safely, resolve conflicts, and "
            "collaborate on shared codebases using Git and GitHub/GitLab workflows "
            "such as pull requests and code review."
        ),
        category="Programming Fundamentals",
        difficulty="Beginner",
        prerequisites=[],
        duration="3-4 days",
        skills_gained=["Git", "Branching & Merging", "Pull Requests", "Conflict Resolution"],
        career_roles=[
            "Software Developer", "DevOps Engineer", "QA Engineer",
            "Data Engineer", "Any Software-Adjacent Role",
        ],
        keywords=["git", "github", "gitlab", "version control"],
        related_skills=["CI/CD", "Code Review"],
        optional_tools=["GitHub", "GitLab", "Bitbucket"],
        learning_outcomes=[
            "Track and version project changes with Git",
            "Collaborate through branches and pull requests",
            "Resolve merge conflicts confidently",
        ],
    ),

    # ============================================================
    # FRONTEND DEVELOPMENT
    # ============================================================
    Course(
        id="html",
        name="HTML",
        description=(
            "Structure web content using semantic HTML5 elements, forms, and "
            "accessible markup patterns that form the foundation of every web page."
        ),
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=[],
        duration="1 week",
        skills_gained=["HTML", "Semantic Markup", "Forms", "Basic Accessibility"],
        career_roles=["Web Developer", "Frontend Developer", "UI Developer"],
        keywords=["html", "markup", "web fundamentals"],
        related_skills=["CSS", "Web Accessibility"],
        optional_tools=["VS Code", "Browser DevTools"],
        learning_outcomes=["Structure a web page with semantic HTML", "Build accessible forms"],
    ),
    Course(
        id="css",
        name="CSS",
        description=(
            "Style and lay out web pages using CSS box model, Flexbox, Grid, and "
            "responsive design techniques for multi-device layouts."
        ),
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=["html"],
        duration="1-2 weeks",
        skills_gained=["CSS", "Flexbox", "CSS Grid", "Responsive Design"],
        career_roles=["Web Developer", "Frontend Developer", "UI Developer"],
        keywords=["css", "styling", "responsive design"],
        related_skills=["HTML", "UI Design"],
        optional_tools=["Tailwind CSS", "Sass"],
        learning_outcomes=["Build responsive layouts with Flexbox and Grid", "Style components consistently"],
    ),
    Course(
        id="javascript",
        name="JavaScript",
        description=(
            "Core JavaScript: variables, functions, closures, the event loop, "
            "asynchronous programming with promises/async-await, and DOM "
            "manipulation for interactive web pages."
        ),
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=["css"],
        duration="3-4 weeks",
        skills_gained=["JavaScript", "DOM Manipulation", "Async/Await", "Closures", "ES6+ Syntax"],
        career_roles=[
            "JavaScript Developer", "Frontend Developer", "Web Developer",
            "Full Stack Developer", "Node.js Developer",
        ],
        keywords=["javascript", "es6", "dom", "async programming"],
        related_skills=["TypeScript", "Node.js"],
        optional_tools=["Node.js", "npm"],
        learning_outcomes=[
            "Manipulate the DOM to build interactive pages",
            "Write and reason about asynchronous JavaScript",
        ],
    ),
    Course(
        id="typescript",
        name="TypeScript",
        description=(
            "Add static typing to JavaScript with interfaces, generics, and type "
            "inference, improving code safety and maintainability in larger codebases."
        ),
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="1-2 weeks",
        skills_gained=["TypeScript", "Interfaces & Types", "Generics", "Type Inference"],
        career_roles=["TypeScript Developer", "Frontend Developer", "Full Stack Developer", "React Developer"],
        keywords=["typescript", "static typing", "type safety"],
        related_skills=["JavaScript", "React"],
        optional_tools=["tsc", "ESLint"],
        learning_outcomes=["Add type safety to an existing JavaScript codebase", "Use generics for reusable types"],
    ),
    Course(
        id="react",
        name="React",
        description=(
            "Build component-based, interactive user interfaces with React: "
            "hooks, state management, component composition, and client-side "
            "routing for single-page applications."
        ),
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="3-4 weeks",
        skills_gained=["React", "Hooks", "Component Composition", "Client-Side Routing", "State Management"],
        career_roles=["React Developer", "Frontend Developer", "Full Stack Developer", "Web Developer", "UI Engineer"],
        keywords=["react", "spa", "component-based ui"],
        related_skills=["TypeScript", "Redux", "Next.js"],
        optional_tools=["Vite", "React Router", "Redux"],
        learning_outcomes=["Build reusable UI components", "Manage state and side effects with hooks"],
    ),
    Course(
        id="angular",
        name="Angular",
        description=(
            "Build large-scale single-page applications with Angular's component "
            "model, dependency injection, RxJS-based reactive patterns, and routing."
        ),
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["typescript"],
        duration="4-5 weeks",
        skills_gained=["Angular", "Dependency Injection", "RxJS", "Component Architecture"],
        career_roles=["Angular Developer", "Frontend Developer", "Full Stack Developer"],
        keywords=["angular", "spa", "enterprise frontend"],
        related_skills=["TypeScript", "RxJS"],
        optional_tools=["Angular CLI"],
        learning_outcomes=["Structure a large Angular application", "Use RxJS for reactive data flows"],
    ),
    Course(
        id="vue",
        name="Vue.js",
        description=(
            "Build reactive user interfaces with Vue's component system, "
            "reactivity model, and the Composition API for scalable frontend apps."
        ),
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="2-3 weeks",
        skills_gained=["Vue.js", "Composition API", "Reactive State", "Single File Components"],
        career_roles=["Vue Developer", "Frontend Developer", "Web Developer"],
        keywords=["vue", "spa", "reactive ui"],
        related_skills=["JavaScript", "TypeScript"],
        optional_tools=["Vite", "Pinia"],
        learning_outcomes=["Build components with Vue's Composition API", "Manage reactive state in Vue"],
    ),
    Course(
        id="frontend_testing",
        name="Frontend Testing",
        description=(
            "Write unit and component tests for modern JavaScript frontends using "
            "Jest and React Testing Library, plus end-to-end tests with Playwright/Cypress."
        ),
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["react"],
        duration="1-2 weeks",
        skills_gained=["Unit Testing", "Component Testing", "End-to-End Testing", "Test-Driven Development Basics"],
        career_roles=["Frontend Developer", "SDET", "QA Engineer", "Automation Test Engineer"],
        keywords=["frontend testing", "jest", "e2e testing"],
        related_skills=["React", "CI/CD"],
        optional_tools=["Jest", "React Testing Library", "Playwright", "Cypress"],
        learning_outcomes=["Write reliable component tests", "Automate end-to-end browser test flows"],
    ),

    # ============================================================
    # BACKEND DEVELOPMENT
    # ============================================================
    Course(
        id="nodejs",
        name="Node.js Backend Development",
        description=(
            "Build server-side applications and REST APIs with Node.js and "
            "Express: routing, middleware, authentication basics, and connecting "
            "to a database."
        ),
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="3-4 weeks",
        skills_gained=["Node.js", "Express", "REST APIs", "Middleware", "Authentication Basics"],
        career_roles=["Node.js Developer", "Backend Developer", "Full Stack Developer", "API Developer"],
        keywords=["node.js", "express", "rest api"],
        related_skills=["PostgreSQL", "MongoDB", "Docker"],
        optional_tools=["Express", "npm", "Postman"],
        learning_outcomes=["Design and implement REST endpoints", "Structure a Node.js backend service"],
    ),
    Course(
        id="django",
        name="Django Web Framework",
        description=(
            "Build full-featured web applications with Django: models, the ORM, "
            "views/templates, the admin interface, and Django REST Framework for APIs."
        ),
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="3-4 weeks",
        skills_gained=["Django", "Django ORM", "Django REST Framework", "MVC/MVT Architecture"],
        career_roles=["Python Developer", "Django Developer", "Backend Developer", "Full Stack Developer"],
        keywords=["django", "python web framework", "orm"],
        related_skills=["Python", "PostgreSQL", "REST APIs"],
        optional_tools=["Django Admin", "Django REST Framework"],
        learning_outcomes=["Build a data-backed web application with Django", "Expose Django models as REST APIs"],
    ),
    Course(
        id="fastapi",
        name="FastAPI",
        description=(
            "Build fast, typed REST APIs in Python with FastAPI: request/response "
            "validation via Pydantic, dependency injection, async endpoints, and "
            "automatic OpenAPI documentation."
        ),
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="2 weeks",
        skills_gained=["FastAPI", "REST APIs", "Pydantic Validation", "Async Endpoints", "OpenAPI/Swagger"],
        career_roles=["Python Developer", "FastAPI Developer", "Backend Developer", "API Developer"],
        keywords=["fastapi", "python api framework", "async"],
        related_skills=["Python", "PostgreSQL", "Docker"],
        optional_tools=["Uvicorn", "Pydantic", "Swagger UI"],
        learning_outcomes=["Build typed, validated REST APIs", "Document APIs automatically with OpenAPI"],
    ),
    Course(
        id="spring_boot",
        name="Spring Boot",
        description=(
            "Build production-grade Java backend services with Spring Boot: "
            "dependency injection, Spring MVC REST controllers, and Spring Data "
            "for database access."
        ),
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["java"],
        duration="4-5 weeks",
        skills_gained=["Spring Boot", "Spring MVC", "Spring Data", "Dependency Injection"],
        career_roles=["Java Developer", "Backend Developer", "Software Engineer"],
        keywords=["spring boot", "java backend", "enterprise java"],
        related_skills=["Java", "PostgreSQL", "REST APIs"],
        optional_tools=["Maven", "Gradle", "Spring Initializr"],
        learning_outcomes=["Build a REST API with Spring Boot", "Connect a Spring application to a database"],
    ),
    Course(
        id="dotnet",
        name="ASP.NET Core",
        description=(
            "Build web APIs and services on the .NET platform with ASP.NET Core: "
            "controllers, middleware, dependency injection, and Entity Framework "
            "for data access."
        ),
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["csharp"],
        duration="3-4 weeks",
        skills_gained=["ASP.NET Core", "Entity Framework", "Web API Development", "Dependency Injection"],
        career_roles=[".NET Developer", "Backend Developer", "Software Engineer"],
        keywords=["asp.net core", ".net", "microsoft backend stack"],
        related_skills=["C#", "SQL Server", "PostgreSQL"],
        optional_tools=["Visual Studio", "Entity Framework Core"],
        learning_outcomes=["Build a web API with ASP.NET Core", "Use Entity Framework for data access"],
    ),

    # ============================================================
    # MOBILE DEVELOPMENT
    # ============================================================
    Course(
        id="android_dev",
        name="Android Development (Kotlin)",
        description=(
            "Build native Android applications with Kotlin: activities, "
            "fragments, Jetpack Compose UI, and integrating REST APIs into a mobile app."
        ),
        category="Mobile Development",
        difficulty="Intermediate",
        prerequisites=[],
        duration="5-6 weeks",
        skills_gained=["Kotlin", "Android SDK", "Jetpack Compose", "Mobile App Architecture"],
        career_roles=["Android Developer", "Mobile App Developer"],
        keywords=["android", "kotlin", "mobile development"],
        related_skills=["REST APIs", "UI Design"],
        optional_tools=["Android Studio"],
        learning_outcomes=["Build and publish a native Android app UI", "Integrate a REST API into a mobile app"],
    ),
    Course(
        id="ios_dev",
        name="iOS Development (Swift)",
        description=(
            "Build native iOS applications with Swift and SwiftUI: view "
            "composition, state management, and integrating network requests "
            "into an iOS app."
        ),
        category="Mobile Development",
        difficulty="Intermediate",
        prerequisites=[],
        duration="5-6 weeks",
        skills_gained=["Swift", "SwiftUI", "iOS App Architecture", "Xcode"],
        career_roles=["iOS Developer", "Mobile App Developer"],
        keywords=["ios", "swift", "swiftui", "mobile development"],
        related_skills=["REST APIs", "UI Design"],
        optional_tools=["Xcode"],
        learning_outcomes=["Build a native iOS app UI with SwiftUI", "Manage app state and navigation"],
    ),
    Course(
        id="react_native",
        name="React Native",
        description=(
            "Build cross-platform mobile apps with React Native, sharing a "
            "component model and much of the codebase between iOS and Android."
        ),
        category="Mobile Development",
        difficulty="Intermediate",
        prerequisites=["react"],
        duration="3-4 weeks",
        skills_gained=["React Native", "Cross-Platform Mobile Development", "Native Modules Basics"],
        career_roles=["React Native Developer", "Mobile App Developer", "Frontend Developer"],
        keywords=["react native", "cross-platform mobile"],
        related_skills=["React", "JavaScript"],
        optional_tools=["Expo"],
        learning_outcomes=["Build a cross-platform mobile app UI", "Share logic between iOS and Android targets"],
    ),
    Course(
        id="flutter_dev",
        name="Flutter Development",
        description=(
            "Build cross-platform mobile apps with Flutter and Dart, using the "
            "widget tree, state management, and platform integration for a single "
            "codebase across iOS and Android."
        ),
        category="Mobile Development",
        difficulty="Intermediate",
        prerequisites=[],
        duration="4-5 weeks",
        skills_gained=["Dart", "Flutter", "Widget Composition", "State Management"],
        career_roles=["Flutter Developer", "Mobile App Developer"],
        keywords=["flutter", "dart", "cross-platform mobile"],
        related_skills=["REST APIs", "UI Design"],
        optional_tools=["Android Studio", "VS Code"],
        learning_outcomes=["Build a Flutter app UI with widgets", "Manage state across a Flutter app"],
    ),

    # ============================================================
    # DATABASES
    # ============================================================
    Course(
        id="sql_fundamentals",
        name="SQL Fundamentals",
        description=(
            "Query and manipulate relational data with SQL: SELECT/JOIN/GROUP BY "
            "queries, filtering, aggregation, and basic schema design concepts."
        ),
        category="Databases",
        difficulty="Beginner",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["SQL", "Joins", "Aggregation", "Filtering & Sorting"],
        career_roles=[
            "Data Analyst", "Business Analyst", "Backend Developer",
            "Database Administrator", "Reporting Analyst", "SQL Developer",
        ],
        keywords=["sql", "relational databases", "querying"],
        related_skills=["PostgreSQL", "Excel"],
        optional_tools=["pgAdmin", "MySQL Workbench"],
        learning_outcomes=["Write multi-table SQL queries", "Aggregate and filter data with SQL"],
    ),
    Course(
        id="postgresql",
        name="PostgreSQL",
        description=(
            "Design relational schemas, write SQL queries, create indexes, manage "
            "transactions, and work with PostgreSQL in production-style applications."
        ),
        category="Databases",
        difficulty="Intermediate",
        prerequisites=["sql_fundamentals"],
        duration="2 weeks",
        skills_gained=[
            "PostgreSQL", "SQL", "Relational Database Design",
            "Indexes", "Transactions", "Query Optimization",
        ],
        career_roles=[
            "Backend Developer", "Database Administrator", "Database Developer",
            "Data Engineer", "Full Stack Developer",
        ],
        keywords=["postgresql", "relational database", "schema design"],
        related_skills=["SQL", "Database Administration"],
        optional_tools=["pgAdmin", "psql"],
        learning_outcomes=["Design a normalized relational schema", "Optimize queries with indexes"],
    ),
    Course(
        id="mongodb",
        name="MongoDB",
        description=(
            "Model and query data in a document-oriented NoSQL database: "
            "collections, documents, aggregation pipelines, and indexing strategies."
        ),
        category="Databases",
        difficulty="Intermediate",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["MongoDB", "NoSQL Data Modeling", "Aggregation Pipelines"],
        career_roles=["Backend Developer", "Node.js Developer", "Database Developer", "Full Stack Developer"],
        keywords=["mongodb", "nosql", "document database"],
        related_skills=["Node.js", "Data Modeling"],
        optional_tools=["MongoDB Compass"],
        learning_outcomes=["Model application data as documents", "Query data with the aggregation pipeline"],
    ),
    Course(
        id="redis_caching",
        name="Redis & Caching Strategies",
        description=(
            "Use Redis as a cache and key-value store to speed up applications: "
            "caching patterns, expiration strategies, and pub/sub messaging basics."
        ),
        category="Databases",
        difficulty="Intermediate",
        prerequisites=[],
        duration="1 week",
        skills_gained=["Redis", "Caching Strategies", "Key-Value Data Modeling", "Pub/Sub Basics"],
        career_roles=["Backend Developer", "Site Reliability Engineer", "Platform Engineer"],
        keywords=["redis", "caching", "performance"],
        related_skills=["Backend Development", "System Design"],
        optional_tools=["Redis CLI"],
        learning_outcomes=["Add a caching layer to an application", "Choose an appropriate cache invalidation strategy"],
    ),

    # ============================================================
    # DATA ENGINEERING
    # ============================================================
    Course(
        id="data_engineering_fundamentals",
        name="Data Engineering Fundamentals",
        description=(
            "Design and build data pipelines: extracting data from sources, "
            "transforming it reliably, and loading it into warehouses, with an "
            "introduction to workflow orchestration."
        ),
        category="Data Engineering",
        difficulty="Intermediate",
        prerequisites=["python", "sql_fundamentals"],
        duration="4-5 weeks",
        skills_gained=["ETL/ELT Pipelines", "Data Pipeline Orchestration", "Data Quality Checks"],
        career_roles=["Data Engineer", "Analytics Engineer", "Data Quality Analyst"],
        keywords=["data engineering", "etl", "pipelines"],
        related_skills=["SQL", "Python", "Cloud Computing"],
        optional_tools=["Apache Airflow", "dbt"],
        learning_outcomes=["Build an end-to-end ETL pipeline", "Add basic data quality validation"],
    ),
    Course(
        id="data_warehousing_etl",
        name="Data Warehousing & ETL Design",
        description=(
            "Design dimensional data warehouse schemas (star/snowflake), and "
            "build ETL jobs that populate them from operational source systems."
        ),
        category="Data Engineering",
        difficulty="Intermediate",
        prerequisites=["sql_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Dimensional Modeling", "Star Schema Design", "ETL Job Design"],
        career_roles=["Data Warehouse Developer", "ETL Developer", "BI Developer", "Data Engineer"],
        keywords=["data warehouse", "dimensional modeling", "etl"],
        related_skills=["SQL", "Business Intelligence"],
        optional_tools=["dbt", "SSIS"],
        learning_outcomes=["Design a star-schema data warehouse", "Build ETL jobs to populate warehouse tables"],
    ),

    # ============================================================
    # DATA ANALYTICS & BUSINESS INTELLIGENCE
    # ============================================================
    Course(
        id="excel_for_analytics",
        name="Excel for Data Analysis",
        description=(
            "Analyze and summarize business data in Excel: formulas, pivot "
            "tables, lookups, and chart-based reporting for everyday analytical work."
        ),
        category="Data Analytics & BI",
        difficulty="Beginner",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["Excel Formulas", "Pivot Tables", "Lookups", "Chart-Based Reporting"],
        career_roles=[
            "Business Analyst", "Data Analyst", "Financial Analyst",
            "Operations Analyst", "Marketing Analyst", "Reporting Analyst",
        ],
        keywords=["excel", "spreadsheet analysis", "reporting"],
        related_skills=["SQL", "Power BI"],
        optional_tools=["Microsoft Excel", "Google Sheets"],
        learning_outcomes=["Summarize datasets with pivot tables", "Build formula-driven reports"],
    ),
    Course(
        id="power_bi_tableau",
        name="Business Intelligence Dashboards (Power BI & Tableau)",
        description=(
            "Build interactive dashboards and reports with Power BI and Tableau: "
            "data modeling, DAX/calculated fields, and visual design for "
            "business stakeholders."
        ),
        category="Data Analytics & BI",
        difficulty="Intermediate",
        prerequisites=["sql_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Power BI", "Tableau", "Dashboard Design", "DAX Basics", "Data Modeling for BI"],
        career_roles=[
            "Business Intelligence Analyst", "BI Developer", "Data Analyst",
            "Reporting Analyst", "Business Analyst",
        ],
        keywords=["power bi", "tableau", "dashboards", "business intelligence"],
        related_skills=["SQL", "Excel", "Data Visualization"],
        optional_tools=["Power BI Desktop", "Tableau Desktop"],
        learning_outcomes=["Build an interactive BI dashboard", "Model data for self-service reporting"],
    ),
    Course(
        id="statistics_fundamentals",
        name="Statistics for Data Analysis",
        description=(
            "Descriptive statistics, probability basics, hypothesis testing, and "
            "correlation/regression concepts needed to reason rigorously about data."
        ),
        category="Data Analytics & BI",
        difficulty="Beginner",
        prerequisites=[],
        duration="2-3 weeks",
        skills_gained=["Descriptive Statistics", "Probability Basics", "Hypothesis Testing", "Correlation & Regression"],
        career_roles=[
            "Data Analyst", "Data Scientist", "Quantitative Analyst",
            "Research Analyst", "Risk Analyst",
        ],
        keywords=["statistics", "probability", "hypothesis testing"],
        related_skills=["NumPy & Pandas", "Machine Learning"],
        optional_tools=[],
        learning_outcomes=["Summarize and interpret data distributions", "Run and interpret a basic hypothesis test"],
    ),
    Course(
        id="numpy_pandas",
        name="NumPy & Pandas",
        description=(
            "Manipulate and analyze structured data efficiently in Python using "
            "NumPy arrays and Pandas DataFrames: cleaning, filtering, grouping, "
            "and merging datasets."
        ),
        category="Data Analytics & BI",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="2-3 weeks",
        skills_gained=["NumPy", "Pandas", "Data Cleaning", "DataFrame Operations", "Data Merging"],
        career_roles=["Data Analyst", "Data Scientist", "Data Engineer", "Quantitative Analyst"],
        keywords=["numpy", "pandas", "data manipulation"],
        related_skills=["Python", "Statistics"],
        optional_tools=["Jupyter Notebook"],
        learning_outcomes=["Clean and reshape tabular data with Pandas", "Perform vectorized computation with NumPy"],
    ),
    Course(
        id="data_visualization",
        name="Data Visualization with Python",
        description=(
            "Communicate insights clearly using Matplotlib and Seaborn: choosing "
            "appropriate chart types, styling for clarity, and avoiding "
            "misleading visual representations."
        ),
        category="Data Analytics & BI",
        difficulty="Intermediate",
        prerequisites=["numpy_pandas"],
        duration="1-2 weeks",
        skills_gained=["Matplotlib", "Seaborn", "Data Visualization", "Chart Design Principles"],
        career_roles=["Data Analyst", "Data Scientist", "Data Visualization Specialist", "Research Analyst"],
        keywords=["data visualization", "matplotlib", "seaborn"],
        related_skills=["Pandas", "Statistics"],
        optional_tools=["Jupyter Notebook"],
        learning_outcomes=["Choose an appropriate chart for a given dataset", "Produce publication-quality plots"],
    ),
    Course(
        id="data_analysis_python",
        name="Applied Data Analysis with Python",
        description=(
            "Apply Pandas and statistical reasoning to end-to-end analysis "
            "projects: exploratory data analysis, drawing conclusions, and "
            "presenting findings to stakeholders."
        ),
        category="Data Analytics & BI",
        difficulty="Intermediate",
        prerequisites=["numpy_pandas", "statistics_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Exploratory Data Analysis", "Data-Driven Storytelling", "Analytical Reporting"],
        career_roles=["Data Analyst", "Business Analyst", "Product Analyst", "Marketing Analyst", "Operations Analyst"],
        keywords=["exploratory data analysis", "eda", "analytics"],
        related_skills=["Pandas", "Statistics", "Data Visualization"],
        optional_tools=["Jupyter Notebook"],
        learning_outcomes=["Run a full exploratory data analysis", "Present data-driven findings clearly"],
    ),

    # ============================================================
    # MACHINE LEARNING & AI
    # ============================================================
    Course(
        id="machine_learning",
        name="Machine Learning",
        description=(
            "Core supervised and unsupervised ML algorithms: regression, "
            "classification, clustering, and model evaluation, implemented with "
            "Scikit-learn on real datasets."
        ),
        category="Machine Learning & AI",
        difficulty="Advanced",
        prerequisites=["numpy_pandas", "statistics_fundamentals"],
        duration="4-6 weeks",
        skills_gained=["Machine Learning", "Scikit-learn", "Model Evaluation", "Feature Engineering"],
        career_roles=["Machine Learning Engineer", "Data Scientist", "AI Engineer", "Applied AI Engineer"],
        keywords=["machine learning", "scikit-learn", "predictive modeling"],
        related_skills=["Statistics", "Deep Learning"],
        optional_tools=["Scikit-learn", "Jupyter Notebook"],
        learning_outcomes=["Train and evaluate supervised ML models", "Engineer features that improve model performance"],
    ),
    Course(
        id="deep_learning",
        name="Deep Learning",
        description=(
            "Build and train neural networks with PyTorch or TensorFlow: "
            "feedforward and convolutional architectures, backpropagation, and "
            "regularization techniques for advanced prediction tasks."
        ),
        category="Machine Learning & AI",
        difficulty="Advanced",
        prerequisites=["machine_learning"],
        duration="6-8 weeks",
        skills_gained=["Deep Learning", "Neural Networks", "PyTorch/TensorFlow", "Model Regularization"],
        career_roles=["Deep Learning Engineer", "Machine Learning Engineer", "AI Engineer", "Computer Vision Engineer"],
        keywords=["deep learning", "neural networks", "pytorch", "tensorflow"],
        related_skills=["Machine Learning", "Computer Vision", "NLP"],
        optional_tools=["PyTorch", "TensorFlow"],
        learning_outcomes=["Design and train a neural network", "Apply regularization to reduce overfitting"],
    ),
    Course(
        id="nlp_fundamentals",
        name="Natural Language Processing",
        description=(
            "Process and model human language: tokenization, embeddings, "
            "sequence models, and using transformer-based models for text "
            "classification and generation tasks."
        ),
        category="Machine Learning & AI",
        difficulty="Advanced",
        prerequisites=["machine_learning"],
        duration="4-5 weeks",
        skills_gained=["NLP", "Text Embeddings", "Transformer Models", "Text Classification"],
        career_roles=["NLP Engineer", "Machine Learning Engineer", "AI Engineer"],
        keywords=["nlp", "natural language processing", "transformers"],
        related_skills=["Deep Learning", "Generative AI"],
        optional_tools=["Hugging Face Transformers"],
        learning_outcomes=["Build a text classification pipeline", "Use pretrained transformer models for NLP tasks"],
    ),
    Course(
        id="computer_vision",
        name="Computer Vision",
        description=(
            "Process and understand images with convolutional neural networks: "
            "image classification, object detection basics, and transfer "
            "learning from pretrained vision models."
        ),
        category="Machine Learning & AI",
        difficulty="Advanced",
        prerequisites=["deep_learning"],
        duration="4-5 weeks",
        skills_gained=["Computer Vision", "Convolutional Neural Networks", "Object Detection Basics", "Transfer Learning"],
        career_roles=["Computer Vision Engineer", "Deep Learning Engineer", "AI Engineer"],
        keywords=["computer vision", "cnn", "image classification"],
        related_skills=["Deep Learning"],
        optional_tools=["PyTorch", "OpenCV"],
        learning_outcomes=["Train an image classification model", "Apply transfer learning from a pretrained model"],
    ),
    Course(
        id="generative_ai_llms",
        name="Generative AI & LLM Applications",
        description=(
            "Build applications on top of large language models: prompt "
            "engineering, retrieval-augmented generation (RAG), embeddings, and "
            "responsible use of generative AI APIs."
        ),
        category="Machine Learning & AI",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="2-3 weeks",
        skills_gained=["Prompt Engineering", "Retrieval-Augmented Generation", "Embeddings", "LLM APIs"],
        career_roles=["Generative AI Engineer", "AI Application Developer", "Applied AI Engineer", "AI Engineer"],
        keywords=["generative ai", "llm", "rag", "prompt engineering"],
        related_skills=["NLP", "Vector Databases"],
        optional_tools=["OpenAI API", "LangChain", "Vector Databases"],
        learning_outcomes=["Design effective prompts for an LLM", "Build a basic RAG pipeline over custom documents"],
    ),
    Course(
        id="mlops_fundamentals",
        name="MLOps Fundamentals",
        description=(
            "Take machine learning models from notebook to production: model "
            "packaging, versioning, containerized deployment, and monitoring "
            "model performance over time."
        ),
        category="Machine Learning & AI",
        difficulty="Advanced",
        prerequisites=["machine_learning", "docker_containers"],
        duration="3-4 weeks",
        skills_gained=["Model Deployment", "Model Versioning", "ML Monitoring", "Containerized ML Serving"],
        career_roles=["MLOps Engineer", "Machine Learning Engineer", "AI Engineer", "Platform Engineer"],
        keywords=["mlops", "model deployment", "ml infrastructure"],
        related_skills=["Machine Learning", "Docker", "Cloud Computing"],
        optional_tools=["MLflow", "Docker", "FastAPI"],
        learning_outcomes=["Package and deploy a trained model as a service", "Set up basic monitoring for a deployed model"],
    ),

    # ============================================================
    # CLOUD COMPUTING
    # ============================================================
    Course(
        id="cloud_fundamentals",
        name="Cloud Computing Fundamentals",
        description=(
            "Core cloud concepts that apply across providers: compute, storage, "
            "networking, IAM, and the shared responsibility model, as a "
            "foundation before specializing in AWS, Azure, or GCP."
        ),
        category="Cloud Computing",
        difficulty="Beginner",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["Cloud Computing Concepts", "IAM Basics", "Cloud Storage", "Shared Responsibility Model"],
        career_roles=[
            "Cloud Engineer", "Cloud Administrator", "DevOps Engineer",
            "Cloud Support Engineer", "Support Engineer", "System Administrator",
        ],
        keywords=["cloud computing", "iam", "cloud fundamentals"],
        related_skills=["Linux", "Networking"],
        optional_tools=[],
        learning_outcomes=["Explain core cloud service models (IaaS/PaaS/SaaS)", "Reason about basic cloud security responsibilities"],
    ),
    Course(
        id="aws_cloud_practitioner",
        name="AWS Cloud Services",
        description=(
            "Provision and manage core AWS services: EC2, S3, IAM, VPC, and "
            "Lambda, applied to deploying and running real workloads on AWS."
        ),
        category="Cloud Computing",
        difficulty="Intermediate",
        prerequisites=["cloud_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["AWS", "EC2", "S3", "IAM Policies", "Lambda Basics"],
        career_roles=["Cloud Engineer", "DevOps Engineer", "Cloud Solutions Engineer", "Site Reliability Engineer"],
        keywords=["aws", "amazon web services", "cloud infrastructure"],
        related_skills=["Cloud Fundamentals", "Terraform"],
        optional_tools=["AWS Console", "AWS CLI"],
        learning_outcomes=["Deploy a workload on EC2", "Configure IAM permissions following least privilege"],
    ),
    Course(
        id="azure_fundamentals",
        name="Microsoft Azure Fundamentals",
        description=(
            "Provision and manage core Azure services: virtual machines, "
            "storage accounts, Azure Active Directory, and resource groups for "
            "running workloads on Azure."
        ),
        category="Cloud Computing",
        difficulty="Intermediate",
        prerequisites=["cloud_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Azure", "Azure Virtual Machines", "Azure Storage", "Azure Active Directory"],
        career_roles=["Cloud Engineer", "Cloud Administrator", "DevOps Engineer"],
        keywords=["azure", "microsoft cloud", "cloud infrastructure"],
        related_skills=["Cloud Fundamentals"],
        optional_tools=["Azure Portal", "Azure CLI"],
        learning_outcomes=["Deploy and manage a VM on Azure", "Configure access with Azure AD"],
    ),
    Course(
        id="terraform_iac",
        name="Infrastructure as Code with Terraform",
        description=(
            "Define and provision cloud infrastructure declaratively with "
            "Terraform: modules, state management, and repeatable, version-"
            "controlled infrastructure deployments."
        ),
        category="Cloud Computing",
        difficulty="Intermediate",
        prerequisites=["cloud_fundamentals"],
        duration="1-2 weeks",
        skills_gained=["Terraform", "Infrastructure as Code", "Terraform State Management", "Modules"],
        career_roles=["DevOps Engineer", "Cloud Engineer", "Platform Engineer", "Infrastructure Engineer"],
        keywords=["terraform", "infrastructure as code", "iac"],
        related_skills=["AWS", "Azure", "CI/CD"],
        optional_tools=["Terraform CLI"],
        learning_outcomes=["Provision cloud resources with Terraform", "Manage Terraform state safely"],
    ),

    # ============================================================
    # DEVOPS & INFRASTRUCTURE
    # ============================================================
    Course(
        id="linux_administration",
        name="Linux System Administration",
        description=(
            "Administer Linux servers: the filesystem, permissions, process "
            "management, shell scripting, and common troubleshooting workflows "
            "for production systems."
        ),
        category="DevOps & Infrastructure",
        difficulty="Beginner",
        prerequisites=[],
        duration="2-3 weeks",
        skills_gained=["Linux CLI", "Shell Scripting", "File Permissions", "Process Management", "Log Troubleshooting"],
        career_roles=[
            "System Administrator", "Linux Administrator", "DevOps Engineer",
            "Cloud Engineer", "Support Engineer", "Site Reliability Engineer",
        ],
        keywords=["linux", "shell scripting", "system administration"],
        related_skills=["Networking", "Cloud Computing"],
        optional_tools=["Bash", "systemd"],
        learning_outcomes=["Administer a Linux server from the command line", "Write basic shell scripts for automation"],
    ),
    Course(
        id="networking_fundamentals",
        name="Networking Fundamentals",
        description=(
            "Core networking concepts: TCP/IP, DNS, HTTP/HTTPS, subnetting, and "
            "diagnosing connectivity issues, as a foundation for infrastructure, "
            "support, and security roles."
        ),
        category="DevOps & Infrastructure",
        difficulty="Beginner",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["TCP/IP", "DNS", "HTTP/HTTPS", "Subnetting", "Network Troubleshooting"],
        career_roles=[
            "Network Administrator", "Network Engineer", "Support Engineer",
            "System Administrator", "Cybersecurity Analyst",
        ],
        keywords=["networking", "tcp/ip", "dns"],
        related_skills=["Linux", "Cybersecurity"],
        optional_tools=["Wireshark", "ping/traceroute"],
        learning_outcomes=["Explain how TCP/IP and DNS resolve a request", "Diagnose basic connectivity issues"],
    ),
    Course(
        id="docker_containers",
        name="Docker & Containerization",
        description=(
            "Package applications into portable containers with Docker: "
            "images, Dockerfiles, volumes, networking, and multi-container apps "
            "with Docker Compose."
        ),
        category="DevOps & Infrastructure",
        difficulty="Intermediate",
        prerequisites=["linux_administration"],
        duration="1-2 weeks",
        skills_gained=["Docker", "Dockerfiles", "Container Networking", "Docker Compose"],
        career_roles=["DevOps Engineer", "Backend Developer", "Site Reliability Engineer", "Platform Engineer"],
        keywords=["docker", "containers", "containerization"],
        related_skills=["Linux", "Kubernetes"],
        optional_tools=["Docker Desktop", "Docker Compose"],
        learning_outcomes=["Containerize an application with a Dockerfile", "Run a multi-service app with Docker Compose"],
    ),
    Course(
        id="kubernetes_orchestration",
        name="Kubernetes",
        description=(
            "Orchestrate containerized applications at scale with Kubernetes: "
            "pods, deployments, services, and basic cluster networking and scaling."
        ),
        category="DevOps & Infrastructure",
        difficulty="Advanced",
        prerequisites=["docker_containers", "networking_fundamentals"],
        duration="3-4 weeks",
        skills_gained=["Kubernetes", "Pods & Deployments", "Services & Ingress", "Cluster Scaling Basics"],
        career_roles=["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer", "Cloud Engineer"],
        keywords=["kubernetes", "k8s", "container orchestration"],
        related_skills=["Docker", "Cloud Computing"],
        optional_tools=["kubectl", "Helm"],
        learning_outcomes=["Deploy an application to a Kubernetes cluster", "Expose a service with Kubernetes networking"],
    ),
    Course(
        id="ci_cd_pipelines",
        name="CI/CD Pipelines",
        description=(
            "Automate build, test, and deployment with continuous integration "
            "and delivery pipelines, using tools such as GitHub Actions or Jenkins."
        ),
        category="DevOps & Infrastructure",
        difficulty="Intermediate",
        prerequisites=["git_version_control", "docker_containers"],
        duration="1-2 weeks",
        skills_gained=["CI/CD", "Pipeline Automation", "Automated Testing in Pipelines", "Deployment Automation"],
        career_roles=["DevOps Engineer", "Release Engineer", "Build Engineer", "Platform Engineer"],
        keywords=["ci/cd", "continuous integration", "continuous delivery"],
        related_skills=["Git", "Docker", "Testing"],
        optional_tools=["GitHub Actions", "Jenkins", "GitLab CI"],
        learning_outcomes=["Build a CI pipeline that runs tests automatically", "Automate deployment on a successful build"],
    ),
    Course(
        id="site_reliability_monitoring",
        name="Monitoring, Logging & Observability",
        description=(
            "Instrument systems for observability: metrics, structured logging, "
            "alerting, and dashboards to detect and diagnose production issues."
        ),
        category="DevOps & Infrastructure",
        difficulty="Intermediate",
        prerequisites=["linux_administration", "cloud_fundamentals"],
        duration="1-2 weeks",
        skills_gained=["Monitoring", "Structured Logging", "Alerting", "Observability Dashboards"],
        career_roles=["Site Reliability Engineer", "DevOps Engineer", "Platform Engineer", "Support Engineer"],
        keywords=["monitoring", "logging", "observability", "sre"],
        related_skills=["Cloud Computing", "Linux"],
        optional_tools=["Prometheus", "Grafana", "ELK Stack"],
        learning_outcomes=["Set up basic metrics and alerting for a service", "Diagnose an incident using logs and dashboards"],
    ),

    # ============================================================
    # CYBERSECURITY
    # ============================================================
    Course(
        id="cybersecurity_fundamentals",
        name="Cybersecurity Fundamentals",
        description=(
            "Core security concepts: the CIA triad, common attack types, "
            "authentication/authorization, and security best practices that "
            "underpin every specialized security role."
        ),
        category="Cybersecurity",
        difficulty="Beginner",
        prerequisites=["networking_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Security Fundamentals", "CIA Triad", "Authentication & Authorization", "Common Attack Types"],
        career_roles=["Cybersecurity Analyst", "Security Analyst", "SOC Analyst", "GRC Analyst"],
        keywords=["cybersecurity", "infosec", "security fundamentals"],
        related_skills=["Networking", "Linux"],
        optional_tools=[],
        learning_outcomes=["Explain core security principles (CIA triad)", "Recognize common attack patterns"],
    ),
    Course(
        id="network_security",
        name="Network Security",
        description=(
            "Secure networks against common threats: firewalls, VPNs, intrusion "
            "detection concepts, and network segmentation strategies."
        ),
        category="Cybersecurity",
        difficulty="Intermediate",
        prerequisites=["cybersecurity_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Firewalls", "VPNs", "Intrusion Detection Basics", "Network Segmentation"],
        career_roles=["Network Security Engineer", "Security Engineer", "Cybersecurity Analyst", "Penetration Tester"],
        keywords=["network security", "firewalls", "vpn"],
        related_skills=["Networking", "Cybersecurity Fundamentals"],
        optional_tools=["Wireshark", "pfSense"],
        learning_outcomes=["Configure basic firewall rules", "Explain how a VPN secures network traffic"],
    ),
    Course(
        id="cloud_security",
        name="Cloud Security",
        description=(
            "Secure cloud workloads and identities: IAM policy design, "
            "encryption at rest/in transit, and shared-responsibility security "
            "controls across cloud providers."
        ),
        category="Cybersecurity",
        difficulty="Intermediate",
        prerequisites=["cybersecurity_fundamentals", "cloud_fundamentals"],
        duration="2 weeks",
        skills_gained=["Cloud IAM Policies", "Encryption Basics", "Cloud Security Posture", "Shared Responsibility Model"],
        career_roles=["Cloud Security Engineer", "Security Engineer", "Cybersecurity Analyst", "Cloud Engineer"],
        keywords=["cloud security", "iam", "encryption"],
        related_skills=["Cloud Computing", "Cybersecurity Fundamentals"],
        optional_tools=["AWS IAM", "Azure AD"],
        learning_outcomes=["Design least-privilege IAM policies", "Apply encryption to data at rest and in transit"],
    ),
    Course(
        id="application_security",
        name="Application Security",
        description=(
            "Identify and remediate common application vulnerabilities (OWASP "
            "Top 10): injection, broken auth, XSS, and secure coding practices."
        ),
        category="Cybersecurity",
        difficulty="Intermediate",
        prerequisites=["cybersecurity_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["OWASP Top 10", "Secure Coding Practices", "Input Validation", "Vulnerability Remediation"],
        career_roles=["Application Security Engineer", "Security Engineer", "Software Developer", "Cybersecurity Analyst"],
        keywords=["application security", "owasp", "secure coding"],
        related_skills=["Web Development", "Cybersecurity Fundamentals"],
        optional_tools=["OWASP ZAP"],
        learning_outcomes=["Identify OWASP Top 10 vulnerabilities in code", "Apply secure coding fixes"],
    ),
    Course(
        id="penetration_testing",
        name="Penetration Testing Fundamentals",
        description=(
            "Ethical hacking methodology: reconnaissance, scanning, exploitation "
            "basics, and reporting findings, using industry-standard tools in a "
            "lab environment."
        ),
        category="Cybersecurity",
        difficulty="Advanced",
        prerequisites=["network_security"],
        duration="4-5 weeks",
        skills_gained=["Penetration Testing Methodology", "Vulnerability Scanning", "Exploitation Basics", "Security Reporting"],
        career_roles=["Penetration Tester", "Vulnerability Analyst", "Security Engineer"],
        keywords=["penetration testing", "ethical hacking", "vulnerability scanning"],
        related_skills=["Network Security", "Application Security"],
        optional_tools=["Nmap", "Metasploit", "Burp Suite"],
        learning_outcomes=["Run a structured penetration test in a lab", "Write a professional vulnerability report"],
    ),
    Course(
        id="incident_response",
        name="Security Incident Response",
        description=(
            "Detect, contain, and remediate security incidents: incident "
            "response lifecycle, evidence handling, and post-incident reporting."
        ),
        category="Cybersecurity",
        difficulty="Intermediate",
        prerequisites=["cybersecurity_fundamentals"],
        duration="2 weeks",
        skills_gained=["Incident Response Lifecycle", "Evidence Handling Basics", "Root Cause Analysis"],
        career_roles=["Incident Response Analyst", "SOC Analyst", "Security Operations Specialist", "Cybersecurity Analyst"],
        keywords=["incident response", "soc", "security operations"],
        related_skills=["Cybersecurity Fundamentals", "Monitoring"],
        optional_tools=["SIEM tools"],
        learning_outcomes=["Follow a structured incident response process", "Document an incident post-mortem"],
    ),

    # ============================================================
    # SOFTWARE TESTING & QA
    # ============================================================
    Course(
        id="software_testing_fundamentals",
        name="Software Testing Fundamentals",
        description=(
            "Core testing concepts: test case design, the testing pyramid, bug "
            "reporting, and manual functional testing techniques that apply "
            "regardless of tooling."
        ),
        category="Software Testing",
        difficulty="Beginner",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["Test Case Design", "Bug Reporting", "Manual Testing", "Testing Pyramid Concepts"],
        career_roles=["QA Engineer", "QA Analyst", "Software Tester", "Quality Analyst"],
        keywords=["software testing", "qa", "manual testing"],
        related_skills=["Test Automation", "Software Development Lifecycle"],
        optional_tools=["Jira", "TestRail"],
        learning_outcomes=["Design effective test cases from requirements", "Write clear, reproducible bug reports"],
    ),
    Course(
        id="test_automation_selenium",
        name="Test Automation with Selenium",
        description=(
            "Automate browser-based functional tests with Selenium WebDriver, "
            "structuring maintainable test suites using the Page Object pattern."
        ),
        category="Software Testing",
        difficulty="Intermediate",
        prerequisites=["software_testing_fundamentals", "python"],
        duration="2-3 weeks",
        skills_gained=["Selenium WebDriver", "Page Object Model", "Automated Regression Testing"],
        career_roles=["Automation Test Engineer", "SDET", "QA Engineer"],
        keywords=["selenium", "test automation", "regression testing"],
        related_skills=["Python", "CI/CD"],
        optional_tools=["Selenium WebDriver", "pytest"],
        learning_outcomes=["Automate a browser-based test suite", "Structure tests with the Page Object pattern"],
    ),
    Course(
        id="api_testing",
        name="API Testing & Automation",
        description=(
            "Test REST APIs systematically: request/response validation, "
            "contract testing, and automating API test suites for CI pipelines."
        ),
        category="Software Testing",
        difficulty="Intermediate",
        prerequisites=["software_testing_fundamentals"],
        duration="1-2 weeks",
        skills_gained=["API Testing", "Postman/Newman", "Contract Testing Basics", "Automated API Test Suites"],
        career_roles=["API Test Engineer", "QA Engineer", "SDET", "Automation Test Engineer"],
        keywords=["api testing", "postman", "rest api validation"],
        related_skills=["REST APIs", "CI/CD"],
        optional_tools=["Postman", "Newman"],
        learning_outcomes=["Design a suite of REST API test cases", "Automate API tests in a CI pipeline"],
    ),

    # ============================================================
    # UI/UX DESIGN
    # ============================================================
    Course(
        id="ux_fundamentals",
        name="UX Fundamentals",
        description=(
            "Human-centered design process: user research methods, personas, "
            "usability heuristics, and turning research into design decisions."
        ),
        category="UI/UX Design",
        difficulty="Beginner",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["User Research", "Personas", "Usability Heuristics", "User Journey Mapping"],
        career_roles=["UX Designer", "UX Researcher", "Product Designer", "Interaction Designer"],
        keywords=["ux", "user research", "usability"],
        related_skills=["UI Design", "Wireframing"],
        optional_tools=[],
        learning_outcomes=["Plan and conduct a basic user research study", "Apply usability heuristics to evaluate a design"],
    ),
    Course(
        id="ui_design_figma",
        name="UI Design with Figma",
        description=(
            "Design interfaces visually in Figma: layout, typography, color "
            "systems, components, and collaborative design workflows."
        ),
        category="UI/UX Design",
        difficulty="Beginner",
        prerequisites=["ux_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Figma", "Visual Design Principles", "Typography", "Component-Based Design"],
        career_roles=["UI Designer", "Product Designer", "Interaction Designer"],
        keywords=["figma", "ui design", "visual design"],
        related_skills=["UX Fundamentals", "Design Systems"],
        optional_tools=["Figma"],
        learning_outcomes=["Design a UI screen in Figma", "Build a reusable component in a design file"],
    ),
    Course(
        id="wireframing_prototyping",
        name="Wireframing & Prototyping",
        description=(
            "Translate ideas into low- and high-fidelity wireframes and "
            "clickable prototypes to validate flows before development begins."
        ),
        category="UI/UX Design",
        difficulty="Beginner",
        prerequisites=["ui_design_figma"],
        duration="1-2 weeks",
        skills_gained=["Wireframing", "Interactive Prototyping", "Usability Testing Basics"],
        career_roles=["UX Designer", "Product Designer", "UI Designer"],
        keywords=["wireframing", "prototyping", "usability testing"],
        related_skills=["UX Fundamentals", "Figma"],
        optional_tools=["Figma", "Balsamiq"],
        learning_outcomes=["Build a clickable prototype from wireframes", "Run a basic usability test on a prototype"],
    ),
    Course(
        id="design_systems",
        name="Design Systems",
        description=(
            "Build and maintain a design system: reusable components, design "
            "tokens, and documentation that keeps product design consistent at scale."
        ),
        category="UI/UX Design",
        difficulty="Intermediate",
        prerequisites=["ui_design_figma"],
        duration="2 weeks",
        skills_gained=["Design Tokens", "Component Libraries", "Design System Documentation"],
        career_roles=["Design Systems Specialist", "Product Designer", "UI Designer"],
        keywords=["design systems", "design tokens", "component libraries"],
        related_skills=["UI Design", "Frontend Development"],
        optional_tools=["Figma", "Storybook"],
        learning_outcomes=["Define reusable design tokens", "Document a component library for reuse"],
    ),

    # ============================================================
    # PRODUCT & BUSINESS ANALYSIS
    # ============================================================
    Course(
        id="business_analysis_fundamentals",
        name="Business Analysis Fundamentals",
        description=(
            "Elicit and document business requirements: stakeholder interviews, "
            "process mapping, and writing clear user stories/requirements "
            "specifications."
        ),
        category="Product & Business Analysis",
        difficulty="Beginner",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["Requirements Gathering", "Process Mapping", "User Stories", "Stakeholder Interviews"],
        career_roles=[
            "Business Analyst", "Systems Analyst", "Solutions Analyst",
            "Product Analyst", "Technical Product Manager",
        ],
        keywords=["business analysis", "requirements", "process mapping"],
        related_skills=["Product Management", "Excel"],
        optional_tools=["Jira", "Confluence"],
        learning_outcomes=["Elicit requirements from stakeholders", "Write clear, testable user stories"],
    ),
    Course(
        id="product_management_fundamentals",
        name="Product Management Fundamentals",
        description=(
            "Define and prioritize product roadmaps: discovery, prioritization "
            "frameworks, writing specs, and working cross-functionally with "
            "engineering and design."
        ),
        category="Product & Business Analysis",
        difficulty="Intermediate",
        prerequisites=["business_analysis_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Product Discovery", "Roadmapping", "Prioritization Frameworks", "Cross-Functional Collaboration"],
        career_roles=["Product Manager", "Technical Product Manager", "Product Analyst"],
        keywords=["product management", "roadmapping", "prioritization"],
        related_skills=["Business Analysis", "UX Fundamentals"],
        optional_tools=["Jira", "Productboard"],
        learning_outcomes=["Prioritize a product backlog", "Write a one-page product spec"],
    ),
    Course(
        id="technical_writing",
        name="Technical Writing",
        description=(
            "Write clear technical documentation: API docs, user guides, and "
            "internal knowledge base articles aimed at a defined audience."
        ),
        category="Product & Business Analysis",
        difficulty="Beginner",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["Technical Documentation", "API Documentation", "Audience-Aware Writing"],
        career_roles=["Technical Writer", "Documentation Specialist", "Developer Advocate"],
        keywords=["technical writing", "documentation"],
        related_skills=["Communication", "APIs"],
        optional_tools=["Markdown", "Confluence"],
        learning_outcomes=["Write a clear how-to guide for a technical audience", "Document a REST API"],
    ),

    # ============================================================
    # IT SUPPORT & SYSTEMS ADMINISTRATION
    # ============================================================
    Course(
        id="it_support_fundamentals",
        name="IT Support Fundamentals",
        description=(
            "Diagnose and resolve common hardware, software, and connectivity "
            "issues, and communicate clearly with end users through a structured "
            "ticketing workflow."
        ),
        category="IT Support & Systems Administration",
        difficulty="Beginner",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["Troubleshooting", "Ticketing Systems", "End-User Communication", "Hardware/Software Basics"],
        career_roles=[
            "IT Support Specialist", "Technical Support Engineer", "Help Desk Specialist",
            "Application Support Engineer", "Support Engineer",
        ],
        keywords=["it support", "help desk", "troubleshooting"],
        related_skills=["Networking", "Linux"],
        optional_tools=["Zendesk", "ServiceNow"],
        learning_outcomes=["Triage and resolve a common support ticket", "Communicate technical issues to non-technical users"],
    ),
    Course(
        id="itil_service_management",
        name="IT Service Management (ITIL)",
        description=(
            "Apply ITIL service management practices: incident, problem, and "
            "change management processes used in enterprise IT support and "
            "operations teams."
        ),
        category="IT Support & Systems Administration",
        difficulty="Intermediate",
        prerequisites=["it_support_fundamentals"],
        duration="1-2 weeks",
        skills_gained=["Incident Management", "Problem Management", "Change Management", "ITIL Framework"],
        career_roles=["IT Administrator", "Production Support Engineer", "Technical Operations Engineer", "Support Engineer"],
        keywords=["itil", "service management", "incident management"],
        related_skills=["IT Support", "Monitoring"],
        optional_tools=["ServiceNow"],
        learning_outcomes=["Follow an ITIL-aligned incident management process", "Assess the impact of a proposed change"],
    ),

    # ============================================================
    # FINANCE & BUSINESS ANALYTICS
    # ============================================================
    Course(
        id="financial_analysis_fundamentals",
        name="Financial Analysis Fundamentals",
        description=(
            "Read and analyze financial statements: income statements, balance "
            "sheets, cash flow, and key financial ratios used to assess "
            "company performance."
        ),
        category="Finance & Business Analytics",
        difficulty="Beginner",
        prerequisites=["excel_for_analytics"],
        duration="2-3 weeks",
        skills_gained=["Financial Statement Analysis", "Financial Ratios", "Cash Flow Analysis"],
        career_roles=["Financial Analyst", "FP&A Analyst", "Investment Analyst", "Financial Data Analyst"],
        keywords=["financial analysis", "financial statements", "ratios"],
        related_skills=["Excel", "Statistics"],
        optional_tools=["Excel"],
        learning_outcomes=["Analyze a company's financial statements", "Calculate and interpret key financial ratios"],
    ),
    Course(
        id="financial_modeling",
        name="Financial Modeling",
        description=(
            "Build financial models in Excel: forecasting, scenario analysis, "
            "and valuation techniques used for budgeting and investment decisions."
        ),
        category="Finance & Business Analytics",
        difficulty="Intermediate",
        prerequisites=["financial_analysis_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Financial Forecasting", "Scenario Analysis", "Valuation Basics", "Excel Modeling"],
        career_roles=["Financial Analyst", "FP&A Analyst", "Investment Analyst", "Risk Analyst"],
        keywords=["financial modeling", "forecasting", "valuation"],
        related_skills=["Financial Analysis", "Excel"],
        optional_tools=["Excel"],
        learning_outcomes=["Build a three-statement financial model", "Run scenario analysis on a forecast"],
    ),
    Course(
        id="risk_analytics",
        name="Risk & Credit Analytics",
        description=(
            "Quantify and model financial risk: credit risk basics, "
            "probability-based risk scoring, and using statistical methods to "
            "support risk decisions."
        ),
        category="Finance & Business Analytics",
        difficulty="Intermediate",
        prerequisites=["statistics_fundamentals", "financial_analysis_fundamentals"],
        duration="2-3 weeks",
        skills_gained=["Credit Risk Basics", "Risk Scoring", "Statistical Risk Modeling"],
        career_roles=["Risk Analyst", "Credit Analyst", "Fraud Analyst", "Financial Analyst"],
        keywords=["risk analytics", "credit risk", "fraud analytics"],
        related_skills=["Statistics", "Financial Analysis"],
        optional_tools=["Excel", "Python"],
        learning_outcomes=["Build a basic credit risk scoring approach", "Apply statistical methods to a risk dataset"],
    ),

    # ============================================================
    # MARKETING & SALES ANALYTICS
    # ============================================================
    Course(
        id="digital_marketing_analytics",
        name="Digital Marketing Analytics",
        description=(
            "Measure and analyze marketing performance: campaign metrics, "
            "funnel analysis, attribution basics, and tools like Google Analytics."
        ),
        category="Marketing & Sales Analytics",
        difficulty="Beginner",
        prerequisites=["excel_for_analytics"],
        duration="1-2 weeks",
        skills_gained=["Campaign Analytics", "Funnel Analysis", "Attribution Basics", "Google Analytics"],
        career_roles=["Marketing Analyst", "Digital Marketing Analyst", "Growth Analyst", "CRM Analyst"],
        keywords=["digital marketing", "marketing analytics", "google analytics"],
        related_skills=["Excel", "SQL"],
        optional_tools=["Google Analytics"],
        learning_outcomes=["Analyze a marketing funnel for drop-off points", "Interpret campaign performance metrics"],
    ),
    Course(
        id="seo_fundamentals",
        name="SEO Fundamentals",
        description=(
            "Improve organic search visibility: keyword research, on-page "
            "optimization, and using SEO analytics tools to track performance."
        ),
        category="Marketing & Sales Analytics",
        difficulty="Beginner",
        prerequisites=["digital_marketing_analytics"],
        duration="1 week",
        skills_gained=["Keyword Research", "On-Page SEO", "SEO Analytics Tools"],
        career_roles=["SEO Analyst", "Digital Marketing Analyst", "Growth Analyst"],
        keywords=["seo", "search engine optimization", "keyword research"],
        related_skills=["Digital Marketing Analytics"],
        optional_tools=["Google Search Console", "SEMrush"],
        learning_outcomes=["Conduct basic keyword research", "Audit a page for on-page SEO improvements"],
    ),
    Course(
        id="crm_salesforce_administration",
        name="Salesforce & CRM Administration",
        description=(
            "Administer a CRM platform: managing records, workflows, reports, "
            "and user access in Salesforce for sales and support operations."
        ),
        category="Marketing & Sales Analytics",
        difficulty="Beginner",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["Salesforce Administration", "CRM Workflows", "CRM Reporting", "User Access Management"],
        career_roles=["Salesforce Administrator", "CRM Administrator", "Sales Operations Analyst", "Revenue Operations Analyst"],
        keywords=["salesforce", "crm", "sales operations"],
        related_skills=["Business Analysis"],
        optional_tools=["Salesforce"],
        learning_outcomes=["Configure CRM workflows and reports", "Manage user roles and access in a CRM"],
    ),

    # ============================================================
    # ENTERPRISE SYSTEMS
    # ============================================================
    Course(
        id="sap_fundamentals",
        name="SAP Fundamentals",
        description=(
            "Navigate and configure core SAP ERP modules, understanding how "
            "enterprise business processes (finance, procurement, inventory) "
            "map onto an ERP system."
        ),
        category="Enterprise Systems",
        difficulty="Intermediate",
        prerequisites=["business_analysis_fundamentals"],
        duration="3-4 weeks",
        skills_gained=["SAP Navigation", "ERP Business Processes", "SAP Module Configuration Basics"],
        career_roles=["ERP Analyst", "SAP Analyst", "Business Systems Analyst"],
        keywords=["sap", "erp", "enterprise systems"],
        related_skills=["Business Analysis"],
        optional_tools=["SAP GUI"],
        learning_outcomes=["Navigate core SAP transactions", "Map a business process onto an ERP workflow"],
    ),

    # ============================================================
    # AUTOMATION & RPA
    # ============================================================
    Course(
        id="rpa_automation",
        name="Robotic Process Automation (RPA)",
        description=(
            "Automate repetitive business workflows with RPA tools: recording "
            "and building bots, handling exceptions, and integrating with "
            "existing enterprise systems."
        ),
        category="Automation & RPA",
        difficulty="Intermediate",
        prerequisites=[],
        duration="2-3 weeks",
        skills_gained=["RPA Bot Design", "Workflow Automation", "Exception Handling in Automation"],
        career_roles=["RPA Developer", "Automation Engineer", "Workflow Automation Developer", "Integration Engineer"],
        keywords=["rpa", "robotic process automation", "workflow automation"],
        related_skills=["Business Analysis", "Python"],
        optional_tools=["UiPath", "Power Automate"],
        learning_outcomes=["Design an automated workflow bot", "Handle exceptions in an automated process"],
    ),

    # ============================================================
    # EMERGING TECHNOLOGY & SPECIALIZED ENGINEERING
    # ============================================================
    Course(
        id="blockchain_fundamentals",
        name="Blockchain Fundamentals",
        description=(
            "Core blockchain concepts: distributed ledgers, consensus "
            "mechanisms, cryptographic hashing, and how smart contracts fit "
            "into decentralized applications."
        ),
        category="Emerging Technology",
        difficulty="Intermediate",
        prerequisites=[],
        duration="2-3 weeks",
        skills_gained=["Blockchain Concepts", "Consensus Mechanisms", "Cryptographic Hashing", "Smart Contract Concepts"],
        career_roles=["Blockchain Developer", "Web3 Developer"],
        keywords=["blockchain", "distributed ledger", "web3"],
        related_skills=["Cryptography Basics", "Solidity"],
        optional_tools=[],
        learning_outcomes=["Explain how a blockchain reaches consensus", "Describe how a smart contract executes"],
    ),
    Course(
        id="smart_contract_solidity",
        name="Smart Contract Development (Solidity)",
        description=(
            "Write and deploy smart contracts with Solidity on Ethereum-"
            "compatible chains, including testing and common security pitfalls."
        ),
        category="Emerging Technology",
        difficulty="Advanced",
        prerequisites=["blockchain_fundamentals"],
        duration="3-4 weeks",
        skills_gained=["Solidity", "Smart Contract Testing", "Smart Contract Security Basics"],
        career_roles=["Smart Contract Developer", "Blockchain Developer", "Web3 Developer"],
        keywords=["solidity", "smart contracts", "ethereum"],
        related_skills=["Blockchain Fundamentals"],
        optional_tools=["Hardhat", "Remix"],
        learning_outcomes=["Write and deploy a basic smart contract", "Identify common smart contract vulnerabilities"],
    ),
    Course(
        id="iot_fundamentals",
        name="IoT Fundamentals",
        description=(
            "Connect and manage networked devices: sensor data collection, "
            "communication protocols (MQTT), and basic edge-to-cloud data pipelines."
        ),
        category="Emerging Technology",
        difficulty="Intermediate",
        prerequisites=[],
        duration="2-3 weeks",
        skills_gained=["IoT Architecture", "Sensor Data Collection", "MQTT", "Edge-to-Cloud Basics"],
        career_roles=["IoT Developer", "Edge Computing Engineer", "Embedded Systems Engineer"],
        keywords=["iot", "internet of things", "mqtt", "sensors"],
        related_skills=["Embedded Systems", "Cloud Computing"],
        optional_tools=["Raspberry Pi", "Arduino"],
        learning_outcomes=["Collect and transmit sensor data via MQTT", "Design a basic edge-to-cloud data flow"],
    ),
    Course(
        id="embedded_systems_c",
        name="Embedded Systems Programming",
        description=(
            "Program microcontrollers close to the hardware in C/C++: GPIO, "
            "interrupts, timers, and real-time constraints typical of embedded "
            "and robotics applications."
        ),
        category="Emerging Technology",
        difficulty="Advanced",
        prerequisites=["cpp"],
        duration="4-5 weeks",
        skills_gained=["Embedded C/C++", "GPIO & Interrupts", "Real-Time Constraints", "Microcontroller Programming"],
        career_roles=["Embedded Systems Engineer", "Robotics Software Engineer", "IoT Developer"],
        keywords=["embedded systems", "microcontrollers", "real-time programming"],
        related_skills=["C++", "IoT"],
        optional_tools=["Arduino", "STM32"],
        learning_outcomes=["Write firmware that reads sensors via GPIO", "Reason about real-time timing constraints"],
    ),
    Course(
        id="game_development_fundamentals",
        name="Game Development Fundamentals",
        description=(
            "Build 2D/3D games with a modern game engine: scene composition, "
            "physics basics, game loops, and scripting gameplay logic."
        ),
        category="Emerging Technology",
        difficulty="Intermediate",
        prerequisites=[],
        duration="4-5 weeks",
        skills_gained=["Game Engine Fundamentals", "Game Loop & Physics Basics", "Gameplay Scripting"],
        career_roles=["Game Developer", "Software Engineer"],
        keywords=["game development", "game engine", "unity", "unreal"],
        related_skills=["C++", "C#"],
        optional_tools=["Unity", "Unreal Engine"],
        learning_outcomes=["Build a simple playable game level", "Script basic gameplay interactions"],
    ),
]

_BY_ID = {c.id: c for c in CATALOGUE}


def get_course(course_id: str) -> Course | None:
    return _BY_ID.get(course_id)


def get_all_courses() -> list[Course]:
    return list(CATALOGUE)





