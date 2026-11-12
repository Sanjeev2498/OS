# 🚀 QUICK START GUIDE

## Run the Application in 3 Steps

### Step 1: Open Terminal
```bash
cd OS_Resource_Manager
```

### Step 2: Run the Application
```bash
python main.py
```

### Step 3: Try It Out!

**Example Session**:
```
Main Menu → 1 (Process Scheduling)
  → 5 (Load Sample Data)
  → 1 (Run FCFS)
  → View Results!
  → 0 (Back)

Main Menu → 4 (Analysis & Comparison)
  → 1 (Compare Scheduling Algorithms)
  → View Comparison Table!
```

---

## 📝 Common Tasks

### Task 1: Compare All Scheduling Algorithms
1. Main Menu → **1** (Process Scheduling)
2. **5** (Load Sample Data)
3. **0** (Back to Main)
4. Main Menu → **4** (Analysis & Comparison)
5. **1** (Compare Scheduling)
6. View comparison table and chart!

### Task 2: Test Memory Allocation
1. Main Menu → **2** (Memory Management)
2. **4** (Load Sample Data)
3. **1** (First Fit)
4. View allocation table!
5. Try **2** (Best Fit) and **3** (Worst Fit)

### Task 3: Check for Deadlocks
1. Main Menu → **3** (Deadlock Handling)
2. **4** (Load Sample Data)
3. **1** (Banker's Algorithm)
4. View safe sequence!

### Task 4: View System Logs
1. Main Menu → **5** (View Logs)
2. See all activity history

---

## 📊 Sample Output Preview

**Scheduling Comparison**:
```
Algorithm      Avg Wait    Avg Turnaround    CPU Util%    
------------------------------------------------------------
FCFS           8.20        13.40            80.77         
SJF            6.60        11.80            84.62         
Priority       7.40        12.60            82.05         
Round Robin    12.60       17.80            73.03         
```

**Memory Allocation**:
```
Process    Size    Block      Status         Fragment
------------------------------------------------------
P1         212     Block-2    Allocated      288
P2         417     Block-5    Allocated      183
P3         112     Block-1    Not Allocated  0
P4         426     Block-3    Not Allocated  0
```

**Banker's Algorithm**:
```
✅ SYSTEM IS IN SAFE STATE
Safe Sequence: P1 → P3 → P0 → P2 → P4
```

---

## 🧪 Run Tests

Verify everything works:
```bash
python tests/test_modules.py
```

Expected output:
```
✅ ALL TESTS PASSED SUCCESSFULLY!
Total: 15/15 tests passed (100%)
```

---

## 🔧 Troubleshooting

**Problem**: Module not found error
**Solution**: Make sure you're in the OS_Resource_Manager directory

**Problem**: No charts generated
**Solution**: Install matplotlib: `pip install matplotlib`

**Problem**: Permission denied
**Solution**: Run from your user directory, not system folders

---

## 📁 Project Files

```
OS_Resource_Manager/
├── main.py              ← START HERE!
├── README.md            ← Full documentation
├── QUICKSTART.md        ← This file
├── PROJECT_REPORT.md    ← Detailed report
├── modules/             ← Core algorithms
├── utils/               ← Helpers
├── data/                ← Sample inputs
├── tests/               ← Test suite
├── output/              ← Results and logs
└── scripts/             ← Bash integration
```

---

## 🎓 For Submission

**What to submit**:
1. ✅ Entire `OS_Resource_Manager/` folder
2. ✅ Screenshots of running application
3. ✅ Test execution results
4. ✅ PROJECT_REPORT.md

**How to demonstrate**:
1. Run `python main.py`
2. Load sample data
3. Run algorithms
4. Show comparison feature
5. Display generated charts
6. Show test results

---

## 💡 Tips

- **Sample data is pre-loaded** - just select option 5 in each module
- **Charts save automatically** to `output/charts/`
- **All activity is logged** to `output/system.log`
- **Use option 0** to go back from any menu
- **Use Ctrl+C** to exit if menu is stuck

---

**Need Help?**
- Check README.md for detailed info
- Look at PROJECT_REPORT.md for technical details
- Run tests to verify everything works
- Check logs in output/system.log

---

**Ready to go!** Just run: `python main.py`
