![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Code Coverage](https://codecov.io/gh/pikulo-kama/kama-tr/branch/master/graph/badge.svg)
# <img src="assets/kama-logo.svg" alt="Kama Logo" width="auto" height="100"/> kama-tr (kamatr)


A lightweight, flexible Python localization library that manages text resources across multiple locales with support for dynamic string formatting and custom resource providers.

## Features

* **Decoupled Architecture:** Separate concerns for data structures, resource loading, and state management.
* **Fallback Mechanism:** Automatically returns the resource key if a translation is missing for the active locale.
* **String Formatting:** Supports positional arguments (placeholders) within translation strings.
* **Singleton Support:** Easy-to-use global helper functions for quick integration.

## Architecture

The library consists of three core components:
1.  **Resources:** Data classes (`TextResource`, `TextTranslation`) representing the localized content.
2.  **Providers:** The logic for loading data (`TextResourceProvider`).
3.  **Manager:** The central registry (`TextResourceManager`) that handles locale state and lookups.



---

## Installation

Ensure your project structure follows this pattern:
```text
kamatr/
├── resource.py  # Contains TextResource, TextTranslation
├── provider.py  # Contains TextResourceProvider
└── manager.py   # Contains TextResourceManager and tr()
