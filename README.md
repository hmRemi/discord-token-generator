# Discord Token Generator

The Discord Token Generator is a Python script designed to automate the process of creating Discord accounts and generating tokens. This project can be useful for various purposes, including testing, automation, and other applications where Discord tokens are required.

![Discord Token Generator](https://img.shields.io/badge/version-1.0.0-FF7F7F)
![Discord Token Generator](https://img.shields.io/badge/author-%E2%9C%9F-FF7F7F)

---

## Features

- **Account Creation:** Automatically creates Discord accounts with random emails and passwords.
- **Token Generation:** Retrieves Discord tokens for the created accounts.
- **Proxy Support:** Utilizes proxy servers for enhanced privacy and avoiding IP restrictions.
- **Captcha Solving:** Solves captchas, if required, using an external service (CapMonster).
- **Multi-Threaded:** Operates with multiple threads to improve the account creation speed.

---

## Milestones

- **10 Stars** - Better Error Handling
- **25 Stars** - Recode in Rust
- **50 Stars** - Suggest wtv

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Getting Started

### Prerequisites

To run the Discord Token Generator, you will need the following:

- Python 3.x
- Requests library
- Access to CapMonster API (for captcha solving)
- Discord-related setup (e.g., proxies and email accounts)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Devuxious/Discord-Token-Generator.git
   ```
  
2. Install the required dependencies:
   
   ```bash
   pip install requests
   ```
   
3. Run the script:
   ```bash
   python generate.py
   ```


## Usage

1. After running the script, it will start creating Discord accounts in multiple threads.
2. The script will automatically handle the creation process, including solving captchas if necessary.
3. Discord tokens for the created accounts will be saved to a file (e.g., tokens.txt).
4. You can customize the number of threads and other settings in the code to suit your requirements.

## Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please follow these steps:

1. **Fork the Project:** Start by forking the project to your own GitHub account using the "Fork" button at the top right of this repository.
2. **Create a New Branch:** Create a new branch in your forked repository. This branch will be dedicated to your feature, enhancement, or bug fix.
3. **Make Changes:** Implement your desired changes, whether it's a new feature, improvement, or fixing a bug. Please ensure your code adheres to the project's coding standards.
4. **Commit Your Changes:** Commit your changes with clear and concise commit messages that describe the purpose of each change.
5. **Push to Your Fork:** Push your changes to your forked repository on GitHub.
6. **Create a Pull Request:** Once you've pushed your changes to your fork, go to the original repository and create a pull request. Provide a detailed description of your changes and why they are valuable.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

---

If you have any questions, issues, or suggestions, feel free to open an [issue](https://github.com/Devuxious/Discord-Token-Generator/issues).


<p align="center">
  <img src="https://img.shields.io/github/license/Devuxious/Discord-Token-Generator.svg?style=for-the-badge&labelColor=black&color=FF7F7F&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/Devuxious/Discord-Token-Generator.svg?style=for-the-badge&labelColor=black&color=FF7F7F&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/Devuxious/Discord-Token-Generator.svg?style=for-the-badge&labelColor=black&color=FF7F7F&logo=python"/>
</p>
