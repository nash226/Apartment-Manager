# Apartment Manager

Apartment Manager is a Flask web application backed by PostgreSQL that allows staff to manage apartments and tenants.  
It supports full CRUD (Create, Read, Update, Delete) functionality for both apartments and tenants, with user authentication, form validation, and pagination.

---

## Requirements & Environment

- **Python**: 3.13.0 
- **PostgreSQL**: 14.19
- **Browser Tested**: Chrome Version 140.0.7339.186 
- **Dependencies**:
  - Flask Version: 3.1.2
  - psycopg2 Version: 2.9.10
  - bcrypt Version: 4.3.0

Make sure Python, PostgreSQL, and Poetry are installed before proceeding.

---

## Installation / Setup

1. **Clone or download the project** to your local machine, unzip the file. 

2. **Navigate into the project folder using your commandline(CLI) / terminal** 

3. **Install dependencies**: in your terminal type: poetry install

4. **Setup Database**: in your terminal/CLI type: psql -U <your_username> -d postgres -f seed.sql
    
5. **Run the application**: in your terminal type: poetry run python app.py or python app.py

6. **Access in your browser**: http://localhost:5003

7. **LOGIN INFORMATION** : username - admin | password - secret123

---

## Tradeoffs / Design Choices 

For this project I used two primary tables in my database design. I decided to create a one-many relationship between my two entities apartments / tenants. I chose to allow multiple tenants in one apartment. As this was more realistic in the sense of roomates and subleases. In reality one tenant can have many apartments so the relationship would be more of a many to many in a more realistic scenario. Since this project asked for a simpler scope and asked to avoid complexity I chose to stick with the one to many relationship. For the sake of simplicity I did not make the naming of the tenants unique so we can add multiple tenants with the same name into the same unit or in multiple units; this was a choice to represent the fact that many names are shared between individuals ie. 'John Smith'. With that being said every new tenant with the same name is treated as a seperate entity in the tenants table. To avoid growing complexity and validations I chose to allow this however in a more real world / production application I would choose to create some unique identifier like date of birth and use that to validate ('no two names with the same dob can be renting the same unit' again this could happen in a rare scenario but its unlikelihood makes me comfortable with a choice like this.)

When designing the CRUD features for both tables I chose to not allow the creation of new tenants in the the tenants table and instead to only allow it within the apartments table. This was done purposefully to avoid the scenario of tenants without apartments (with the additional not null constraint on the tenants table for their foreign key) but also as a conscious design decision; for a property manager I wanted them to add tenants when there was an availibility in the apartment unit so it made the most sense to keep the creation of new tenants constrained within vacant units or adding them to occupied apartments. 

Also when deciding how I wanted to design my user flow I consciously made a couple decisions about how I would redirect users after they had completed certain CRUD operations. For example when adding a tenant to a unit I would redirect them back to apartments page because it made sesnse for them to see the updates of the apartment table even though they are adding a tenant. However when they chose to edit or delete a tenant from the apartments page I would redirect the user towards the tenants page since they are updating information about a tenant and may want to see that within the context of the rest of their tenants.