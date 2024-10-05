# Requested changes for Software Development Topics Workshop 01
Inside the SINGLETON.txt file is the explanation of the choice of python singleton design pattern for better handling of instances.

# Usability

## Completed Aspects
- We observed that the registration interface for employees and companies is well-structured, facilitating data entry.
- We noticed that navigation is intuitive, allowing users to easily find job vacancies and their applications.

## Aspects to Improve
- We believe that improving the visibility of success and error messages could facilitate user understanding of the actions performed.
- We identified that accessibility could be strengthened by ensuring forms are usable with a keyboard and compatible with screen readers.

# Compatibility

## Completed Aspects
- We observed that the use of Django ensures good compatibility with different databases and deployment in various environments.
- We noticed that HTML and CSS templates follow web standards, ensuring proper display across multiple browsers.

## Aspects to Improve
- We believe that testing across multiple browsers and devices is essential to ensure consistent user interface functionality.
- We identified that implementing a responsive design could enhance the experience on mobile devices.

# Performance

## Completed Aspects
- We observed that optimized queries using `select_related` and `prefetch_related` improve performance when accessing related data.
- We noticed that separating logic into a service file helps maintainability and can enhance performance.

## Aspects to Improve
- We believe that improving file handling, such as vacancy documents, could reduce loading times by considering more efficient storage strategies.
- We identified that implementing caching for the most visited pages, like the job listing, could reduce the load on the database.

# Security

## Completed Aspects
- We observed that using `django.contrib.auth` to handle authentication and permissions is a safe and recommended practice.
- We noticed that validators are used in forms, preventing invalid entries and improving data integrity.

## Aspects to Improve
- We believe it is essential to ensure that all POST requests include a CSRF token for enhanced security.
- We identified that stricter validations for uploaded files should be implemented, limiting allowed types and sizes.
