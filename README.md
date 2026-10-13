# Python Bootcamp

CSC10014 · Computational Thinking · Git & GitHub for Team Projects

## 👥 Team Members

- `long_th`
- `dieu_sp`
- `vy_th`
- `han_htg`
- `truyen_lp`
- `nhat_npm`
- `nhat_dm`

---

## 📁 Repository Structure

```text
python-bootcamp/
├── README.md               # Rules, team members, how to run tests
├── PROGRESS.md             # One row per member per week (links to PRs)
├── members/
│   ├── long_th/            # Member folder (GitHub username, hyphens replaced with underscores)
│   │   ├── w1/
│   │   ├── w2/
│   │   └── w3/
│   ├── dieu_sp/
│   ├── vy_th/
│   ├── han_htg/
│   ├── truyen_lp/
│   ├── nhat_npm/
│   └── nhat_dm/
├── shared/                 # Team code (T-W2, T-W3)
│   ├── contract.py
│   └── study_planner/
└── tests/                  # Tests provided by the instructor
    ├── test_w1.py
    ├── test_w2.py
    └── test_w3.py
```

---

## 📜 Rules

1. **Folder Naming**:
   - Folder names in `members/` use underscores (e.g. `long_th`, not `long-th`) because Python cannot import a module whose name contains hyphens.
2. **Individual Ownership**:
   - Each member writes code **only in their own folder** (`members/<member_id>/`) for individual homework (`w1/`, `w2/`, `w3/`). This prevents merge conflicts and makes authorship clear.
3. **Shared Code**:
   - Shared team code for `T-W2` and `T-W3` is located in `shared/` (`shared/contract.py` and `shared/study_planner/`).
4. **Git Workflow & PRs**:
   - Work on feature branches and submit code via Pull Requests (PRs).
   - After opening a PR, update `PROGRESS.md` with the link to your PR and status.

---

## 🧪 How to Run Tests

### Prerequisites

Make sure you have Python 3.10+ installed and install required test dependencies:

```bash
pip install pytest
```

### Running All Tests

To run the complete test suite:

```bash
pytest
```

### Running Week-Specific Tests

```bash
# Week 1 tests
pytest tests/test_w1.py

# Week 2 tests
pytest tests/test_w2.py

# Week 3 tests
pytest tests/test_w3.py
```

### Running Tests for a Specific Member

Use pytest keyword filtering `-k`:

```bash
pytest tests/test_w1.py -k "long_th"
```