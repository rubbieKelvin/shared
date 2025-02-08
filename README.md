## Introduction

Setting up new Django projects often involves repetitive tasks and boilerplate code, which can slow down development and lead to inconsistencies across projects. This shared library was created to address these challenges and enhance the developer experience (DX).

> NOTE
> This library is unstable, everything works fine but changes are inevitable, so watch out for changes

### Key Objectives

- **Consistency**: Maintain consistent practices and structures across different Django projects.
- **Productivity**: Eliminate redundant tasks and boilerplate code to accelerate project development.
- **Best Practices**: Incorporate best practices and proven solutions for common development tasks.
- **Flexibility**: Offer configurable components to adapt to project-specific requirements.
- **Sustainability**: Keep the library evolving to embrace changes in Django and emerging development trends.

By utilizing this library, you can streamline your workflow, reduce repetitive work, and ensure that your Django projects adhere to best practices, all while maintaining flexibility and adaptability for your specific project needs.

## Features

### 1. Seamless API Views

Create API views effortlessly with built-in exception handling and straightforward request body validation. This feature simplifies the process of setting up API endpoints while ensuring robust error handling and validation.

### 2. Extended Model Features

Enhance your Django models with extended functionalities, including easy serialization without the need for specifying custom classes. This feature streamlines the serialization process, reducing the need for repetitive code.

### 3. Postman Documentation Generation

Automatically generate Postman documentation from your API views and seamlessly import it into your Postman workspace. This simplifies the task of creating API documentation and keeps it in sync with your codebase.

### 4. Request Body Validation with Pydantic

Effortlessly validate request bodies using Pydantic, a powerful data validation and parsing library. This feature ensures that incoming data meets the expected format, enhancing the security and reliability of your Django applications.

## Installation

To integrate this library into your project, follow these steps:

### Option 1. Clone the Repository

Clone this repository into your project directory:

```shell
git clone https://github.com/rubbieKelvin/shared
```

This method is suitable when you want to keep your library up-to-date by pulling changes from the remote repository.

### Option 2. Add as a Git Submodule

If you have a fork of this library and want to keep it linked to your project while also receiving updates, you can add it as a Git submodule. Use the following command within your project directory:

```shell
git submodule add https://github.com/rubbieKelvin/shared shared-library
```

#### Removing the submodule
If you wish to remove the submodule you'll nee to follow these steps (yeahm it's quite lengthy)
To remove the submodule and delete the `shared-library` folder, follow these steps:

1. **Remove the submodule entry from `.gitmodules`**  
   ```sh
   git config -f .gitmodules --remove-section submodule.shared-library
   ```

2. **Remove the submodule from `.git/config`**  
   ```sh
   git config -f .git/config --remove-section submodule.shared-library
   ```

3. **Unstage the submodule and remove it from tracking**  (if it was commited)  
   ```sh
   git rm --cached shared-library
   ```

4. **Delete the actual submodule folder**  
   ```sh
   rm -rf shared-library
   ```

5. **Remove the submodule from Git history** (optional, if you committed it)  
   ```sh
   git commit -m "Removed shared-library submodule"
   ```

6. **Remove the `shared-library` entry from `.git/modules`**  
   ```sh
   rm -rf .git/modules/shared-library
   ```

After this, the submodule should be completely removed from your repository. If you haven't committed it yet, just running steps 1-4 should be enough.

This submodule is a convenient way to manage an external codebase within your project.

### 3. Download from GitHub

If you prefer a one-time download, you can grab the library as a ZIP file from GitHub. After downloading, extract the contents and place them in your project folder.

> Please note that this library is not yet available on the Python Package Index (PyPI) but may become accessible once it reaches a stable version and undergoes extensive testing in development environments.

## Getting Started

- [Creating endpoint](./docs/creating-endpoints.md)
- [Validating request body](./docs/validating-request-body.md)
- [Defining a model](./docs/defining-models.md)
- [Serializing models](./docs/serializing-models.md)
- [Generating docs](./docs/generating-docs.md)

## Contributions

I welcome contributions from the open-source community to enhance and improve this library. Whether you want to fix a bug, add a feature, or suggest improvements, your contributions are highly valued. Here's how you can get involved:

### Reporting Issues

If you encounter a bug or have a suggestion, please [create an issue](https://github.com/rubbieKelvin/shared/issues/new) on my issue tracker. When creating an issue, provide as much detail as possible, including a clear description, steps to reproduce, and any relevant error messages.

### Pull Requests

If you'd like to contribute code changes, please follow these steps:

1. **Fork the Repository**: Start by forking my repository on GitHub.

2. **Create a Branch**: Create a new branch for your changes. Use a descriptive branch name that relates to the issue or feature you're working on.

3. **Make Changes**: Implement your changes, ensuring that your code adheres to my coding standards.

4. **Tests**: If applicable, write tests to verify your changes.

5. **Documentation**: Update the documentation to reflect your changes, including code comments, README updates, or any other relevant documentation files.

6. **Commit Changes**: Commit your changes with clear and concise commit messages.

7. **Push Changes**: Push your branch to your forked repository on GitHub.

8. **Pull Request**: Open a pull request from your branch to the main repository. In the pull request description, explain the purpose of your changes and reference any related issues.

### Coding Guidelines

To maintain code consistency, follow best practices, including code style, naming conventions, and code structure.

### Review Process

After you submit a pull request, it will undergo a review process. I'll provide feedback and work with you to ensure your contributions align with the project's goals.

I'm excited to collaborate with you, and I appreciate your contributions to make this library even better!

Thank you for being a part of the open-source community. Your efforts are valuable, and they help us improve this library for everyone.

## Acknowledgments

This library would not have been possible without the fantastic work of the open-source community and the following projects:

- [Django](https://www.djangoproject.com/): A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- [Django REST framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs on top of Django.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and parsing using Python type hints.
- [pytest](https://docs.pytest.org/en/latest/): A testing framework that makes it easy to write simple and scalable test cases.

I express my gratitude to the developers and contributors of these projects for providing invaluable tools and resources that have greatly facilitated the development of this library.
