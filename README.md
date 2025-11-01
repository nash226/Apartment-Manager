# Apartment Manager

Apartment Manager is a comprehensive application designed to help property managers track, organize, and manage apartment complexes, tenants, leases, and maintenance requests. Built with Python, this project leverages modern web frameworks and database integrations to deliver an efficient management solution.

## Features

- **Tenant Management**: Add, update, and remove tenant information.
- **Lease Tracking**: Monitor lease agreements, start/end dates, and document uploads.
- **Maintenance Requests**: Log and manage repair and maintenance tickets.
- **Unit Management**: Organize apartments, assign tenants, and track occupancy status.
- **Reporting**: Generate reports on occupancy, rent collection, and maintenance activities.
- **User-friendly Interface**: Responsive web templates for easy interaction.
- **Database Integration**: Seamless data storage and retrieval.

## Getting Started

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nash226/Apartment-Manager.git
   cd Apartment-Manager
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Set up the database:

   - Use `seed.sql` to initialize your database schema and seed data.

   ```bash
   sqlite3 apartment_manager.db < seed.sql
   ```

4. Run the application:

   ```bash
   poetry run python app.py
   ```

5. Access the web interface at `http://localhost:5000`

### Project Structure

- `app.py` - Main application entry point.
- `database.py` - Database connection and query helpers.
- `utils.py` - Utility functions.
- `src/` - Core modules and business logic.
- `templates/` - HTML templates for the web interface.
- `tests/` - Unit and integration tests.
- `pyproject.toml` & `poetry.lock` - Project and dependency management.

## Contributing

Contributions are welcome! Please open issues or submit pull requests with improvements or bug fixes. For major changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License.

## Author

Created by [nash226](https://github.com/nash226).

---

For questions or support, please open an issue in this repository.
