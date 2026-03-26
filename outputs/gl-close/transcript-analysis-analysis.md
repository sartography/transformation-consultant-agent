# Process Analysis: General Ledger Month-End Close Process

## Executive Summary
The General Ledger Month-End Close process is an 8-business-day process managed by the Corporate Controller and four staff accountants, involving coordination with multiple departments (AP, AR, Payroll, Inventory, Warehouse) to close the books and produce management reporting. The process is heavily manual, relying on Excel templates and manual data entry into SAP, with significant pain points around journal entry preparation, account reconciliations, and cross-departmental dependencies.

## Process Steps

### Step 1: Publish Close Calendar
- **Actor/Role**: Corporate Controller (Rachel Martinez) and Accounting Team
- **Description**: Close calendar is published approximately two weeks before each month-end close, containing all deadlines for each team
- **Input**: Upcoming month-end date
- **Output**: Published close calendar with deadlines for all teams
- **Duration/Timing**: Completed approximately 2 weeks before month-end
- **Pain Points**: None mentioned for this step

### Step 2: Lock Prior Period in ERP
- **Actor/Role**: Corporate Controller
- **Description**: Lock the prior month period in SAP to prevent any transactions from being posted to the closed month
- **Input**: First business day after month-end
- **Output**: Locked period in SAP
- **Duration/Timing**: First business day after month-end (Day 1)
- **Pain Points**: None mentioned for this step

### Step 3: Send Close Kickoff Email
- **Actor/Role**: Corporate Controller
- **Description**: Send email to all department heads reminding them of their close deadlines
- **Input**: Locked period and close calendar
- **Output**: Kickoff email sent to department heads
- **Duration/Timing**: Day 1
- **Pain Points**: None mentioned for this step

### Step 4: AP Invoice Entry
- **Actor/Role**: Accounts Payable (Tom and team of 3)
- **Description**: AP team ensures all invoices are entered into the system
- **Input**: All invoices received for the closed month
- **Output**: All invoices entered in system
- **Duration/Timing**: Must be completed by end of Day 1
- **Pain Points**: None mentioned for this specific step

### Step 5: AR Cash Receipt Application
- **Actor/Role**: Accounts Receivable (Sarah and team of 2)
- **Description**: AR team applies all cash receipts to customer accounts
- **Input**: All cash receipts for the closed month
- **Output**: All cash receipts applied
- **Duration/Timing**: Must be completed by Day 1
- **Pain Points**: None mentioned for this specific step

### Step 6: Payroll Confirmation
- **Actor/Role**: Payroll Department
- **Description**: Payroll confirms that the final payroll for the month has posted to the GL
- **Input**: Final payroll run for the month
- **Output**: Confirmation that payroll has posted
- **Duration/Timing**: Must be completed by Day 1
- **Pain Points**: None mentioned for this specific step

### Step 7: AP Three-Way Match and Accruals
- **Actor/Role**: Accounts Payable (Tom and team of 3)
- **Description**: AP runs three-way match process (invoice, purchase order, receipt) and posts accruals for invoices received but not yet entered
- **Input**: All invoices, purchase orders, and receipts
- **Output**: Matched invoices posted; accruals for unmatched invoices
- **Duration/Timing**: Days 2-3 (Sub-ledger close phase)
- **Pain Points**: 30-40% of approximately 200 monthly invoices have discrepancies (wrong price, wrong quantity, missing PO); each discrepancy requires research, vendor/requester contact, and resolution which can take days; many invoices must be accrued to meet close deadline

### Step 8: AR Aging Review and Reserve Analysis
- **Actor/Role**: Accounts Receivable (Sarah and team) with Corporate Controller
- **Description**: AR reviews the aging report and discusses with Controller any reserves needed for doubtful accounts
- **Input**: AR aging report
- **Output**: Determined reserves for doubtful accounts
- **Duration/Timing**: Days 2-3 (Sub-ledger close phase)
- **Pain Points**: None mentioned for this specific step

### Step 9: Fixed Assets Depreciation
- **Actor/Role**: Maria (Fixed Assets/GL accountant)
- **Description**: Run automated depreciation calculation in SAP for all fixed assets
- **Input**: Fixed asset master data
- **Output**: Depreciation entries posted
- **Duration/Timing**: Days 2-3 (Sub-ledger close phase)
- **Pain Points**: None mentioned (noted as automated in SAP)

### Step 10: Inventory Valuation Adjustments
- **Actor/Role**: Warehouse Team with Accounting Team
- **Description**: Process inventory valuation adjustments for physical counts or write-offs
- **Input**: Physical count results, write-off documentation
- **Output**: Inventory valuation adjustment entries
- **Duration/Timing**: Days 2-3 (Sub-ledger close phase)
- **Pain Points**: Coordination required between warehouse team and accounting; if AP is late, it delays everything downstream

### Step 11: Prepare Recurring Journal Entries
- **Actor/Role**: Staff Accountants (4)
- **Description**: Prepare approximately 60 recurring journal entries using Excel templates, calculate amounts, then manually key entries into SAP
- **Input**: Excel templates, source data for calculations
- **Output**: Prepared journal entries in Excel
- **Duration/Timing**: Days 4-5 (Journal entry phase)
- **Pain Points**: Excel templates are inconsistent quality ("all over the place"); some templates are old with broken formulas; manual data entry from Excel to SAP creates risk of errors (fat-fingering numbers); errors have occurred including $50,000 prepaid expense to wrong account and $15,000 transposed digit variance

### Step 12: Prepare Non-Recurring Journal Entries
- **Actor/Role**: Staff Accountants (4)
- **Description**: Prepare 20-30 non-recurring journal entries for period-specific adjustments (prepaid expenses, accrued expenses, deferred revenue recognition, intercompany eliminations)
- **Input**: Period-specific transaction data and supporting documentation
- **Output**: Prepared non-recurring journal entries in Excel
- **Duration/Timing**: Days 4-5 (Journal entry phase)
- **Pain Points**: Same as Step 11 - manual Excel-to-SAP process prone to errors

### Step 13: Review and Approve Journal Entries
- **Actor/Role**: Corporate Controller
- **Description**: Review and approve each journal entry before it posts; entries are in "parked" status until Controller releases them
- **Input**: All prepared journal entries (60 recurring + 20-30 non-recurring)
- **Output**: Approved and posted journal entries
- **Duration/Timing**: Days 4-5 (Journal entry phase)
- **Pain Points**: High volume of manual review required; errors sometimes not caught until later (e.g., external auditors finding misclassified expenses)

### Step 14: Prepare Account Reconciliations
- **Actor/Role**: Staff Accountants (4)
- **Description**: Prepare reconciliations for approximately 150 balance sheet accounts using Excel; download GL balance from SAP, export bank statements from bank portal, manually compare in spreadsheet templates; attach supporting documentation as PDFs
- **Input**: GL balances from SAP, bank statements, supporting documentation
- **Output**: Completed account reconciliations in Excel with supporting documents
- **Duration/Timing**: Days 6-7 (Reconciliation phase); actual reconciliation work takes 2 days but back-and-forth when items don't tie can add 1-2 additional days
- **Pain Points**: Entirely manual process using Excel; no workflow system (just email notifications); time-consuming manual comparison; reconciliation issues can significantly delay close (e.g., $23,000 bank difference took almost a full day to resolve; $15,000 wire transfer timing difference)

### Step 15: Prepare Bank Reconciliations
- **Actor/Role**: Staff Accountants (4)
- **Description**: Reconcile 12 bank accounts to the penny using Excel templates
- **Input**: Bank statements, GL cash balances
- **Output**: Bank reconciliations tied to the penny
- **Duration/Timing**: Days 6-7 (Reconciliation phase)
- **Pain Points**: Must tie to the penny; timing differences between bank posting and GL recording can cause significant delays in resolution (e.g., wire transfers posted on different dates)

### Step 16: Review Account Reconciliations
- **Actor/Role**: Corporate Controller
- **Description**: Review all account reconciliations prepared by staff accountants
- **Input**: Completed reconciliations with supporting documentation
- **Output**: Reviewed and approved reconciliations
- **Duration/Timing**: Days 6-7 (Reconciliation phase)
- **Pain Points**: Manual review process; documentation quality issues noted by auditors (supporting schedules don't clearly tie to GL, missing signatures/dates)

### Step 17: Approve Bank Reconciliations
- **Actor/Role**: Corporate Controller and CFO
- **Description**: Two-signature approval required for bank reconciliations for accounts over $100,000
- **Input**: Completed bank reconciliations
- **Output**: Approved bank reconciliations with two signatures
- **Duration/Timing**: Days 6-7 (Reconciliation phase)
- **Pain Points**: None mentioned for this specific step

### Step 18: Review Trial Balance
- **Actor/Role**: Corporate Controller
- **Description**: Review the trial balance and check that all key accounts look reasonable compared to prior periods
- **Input**: Trial balance from SAP
- **Output**: Validated trial balance
- **Duration/Timing**: Day 8 (Final review and reporting)
- **Pain Points**: Manual review process; time pressure can cause items to be skipped

### Step 19: Run Variance Analysis
- **Actor/Role**: Corporate Controller
- **Description**: Compare actuals to budget and prior year for every P&L line item in Excel; identify variances over 10% or $25,000 and write explanations; chase down department heads for variance explanations
- **Input**: Trial balance, budget data, prior year data
- **Output**: Variance analysis with explanations in Excel workbook
- **Duration/Timing**: Day 8; approximately half a day spent writing explanations
- **Pain Points**: Time-consuming manual process; requires chasing department heads for explanations

### Step 20: Prepare Management Reporting Package
- **Actor/Role**: Corporate Controller
- **Description**: Prepare management reporting package for CFO and executive team
- **Input**: Trial balance, variance analysis, reconciliations
- **Output**: Management reporting package
- **Duration/Timing**: Day 8 (Final review and reporting)
- **Pain Points**: None mentioned for this specific step

### Step 21: Lock Period in SAP
- **Actor/Role**: Corporate Controller
- **Description**: If everything looks good, lock the period in SAP to finalize the close
- **Input**: Completed and reviewed financial statements
- **Output**: Locked period in SAP; close complete
- **Duration/Timing**: Day 8
- **Pain Points**: None mentioned for this specific step

### Step 22: Update Close Checklist (Ongoing)
- **Actor/Role**: All team members
- **Description**: Update Excel close checklist with approximately 80 line items showing responsibility, deadline, and completion status
- **Input**: Completion of individual tasks
- **Output**: Updated checklist
- **Duration/Timing**: Throughout close process; Controller checks twice daily
- **Pain Points**: Not automated; if someone forgets to update, Controller doesn't know there's a problem until asking questions; reactive rather than proactive

### Step 23: Daily Standup Call (Ongoing)
- **Actor/Role**: All team members involved in close
- **Description**: Daily standup call at 9 AM during close week where everyone reports their status
- **Input**: Individual progress on close tasks
- **Output**: Status updates and issue identification
- **Duration/Timing**: Daily at 9 AM during close week (Days 1-8)
- **Pain Points**: Items still slip through despite daily calls

## Actors and Roles

| Role | Responsibilities | Systems Used |
|------|-----------------|--------------|
| Corporate Controller (Rachel Martinez) | Overall process ownership; lock/unlock periods; send kickoff communications; review and approve all journal entries; review all reconciliations; approve bank reconciliations; review trial balance; perform variance analysis; prepare management reporting; monitor close checklist | SAP (ERP), Excel, Email, Bank Portal |
| Staff Accountants (4) | Prepare recurring and non-recurring journal entries; prepare account reconciliations; prepare bank reconciliations; update close checklist | SAP (ERP), Excel, Bank Portal |
| Accounts Payable Manager (Tom) and Team (3) | Enter all invoices by Day 1; run three-way match process; post accruals for unmatched invoices; resolve invoice discrepancies | SAP (ERP) |
| Accounts Receivable Manager (Sarah) and Team (2) | Apply all cash receipts by Day 1; review aging report; determine doubtful account reserves | SAP (ERP) |
| Fixed Assets/GL Accountant (Maria) | Run automated depreciation in SAP; GL work | SAP (ERP) |
| Payroll Department | Confirm final payroll posted to GL | SAP (ERP) |
| Warehouse Team | Perform physical inventory counts; provide write-off documentation; work with accounting on valuation adjustments | SAP (ERP) |
| Department Heads | Provide variance explanations; meet close deadlines | Not specified |
| CFO | Co-approve bank reconciliations over $100,000; receive management reporting package | Not specified |
| Executive Team | Receive management reporting package | Not specified |

## Decision Points

### Decision Point 1: Invoice Matching Status
- **Location in Process**: After Step 7 (AP Three-Way Match)
- **Condition**: Whether invoice matches purchase order and receipt (price, quantity, PO existence)
- **Outcomes**:
  - **Path A**: Invoice matches (60-70% of invoices) → Post invoice
  - **Path B**: Invoice has discrepancy (30-40% of invoices) → Research discrepancy, contact vendor/requester, resolve issue, then post or accrue
- **Decision Maker**: AP team based on system matching rules

### Decision Point 2: Variance Threshold
- **Location in Process**: After Step 19 (Variance Analysis)
- **Condition**: Whether variance exceeds 10% or $25,000
- **Outcomes**:
  - **Path A**: Variance under threshold → No explanation required
  - **Path B**: Variance over threshold → Written explanation required from department head
- **Decision Maker**: System-enforced threshold rule

### Decision Point 3: Bank Reconciliation Approval Authority
- **Location in Process**: After Step 15 (Bank Reconciliations)
- **Condition**: Bank account balance threshold of $100,000
- **Outcomes**:
  - **Path A**: Account balance under $100,000 → Controller approval only
  - **Path B**: Account balance over $100,000 → Controller and CFO approval required
- **Decision Maker**: System-enforced based on account balance

### Decision Point 4: Journal Entry Posting
- **Location in Process**: After Step 13 (Review and Approve Journal Entries)
- **Condition**: Controller approval of parked journal entries
- **Outcomes**:
  - **Path A**: Controller approves → Entry posts to GL
  - **Path B**: Controller rejects → Entry returned to preparer for correction
- **Decision Maker**: Corporate Controller

### Decision Point 5: Period Lock
- **Location in Process**: After Step 20 (Management Reporting Package)
- **Condition**: Whether all reviews are complete and financials look reasonable
- **Outcomes**:
  - **Path A**: Everything looks good → Lock period in SAP (Step 21)
  - **Path B**: Issues identified → Resolve issues before locking
- **Decision Maker**: Corporate Controller

## Systems and Tools

| System | Purpose | Integration Points |
|--------|---------|-------------------|
| SAP (ERP) | General ledger system; period locking; transaction posting; depreciation calculation; trial balance generation | Steps 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 21 |
| Excel | Journal entry templates; account reconciliation templates; variance analysis; close checklist; management reporting | Steps 11, 12, 13, 14, 15, 19, 20, 22 |
| Email | Close kickoff communications; notification when reconciliations ready for review | Steps 3, 14 |
| Bank Portal | Export bank statements for reconciliation | Steps 14, 15 |
| Shared Drive | Store reconciliation folders, supporting documentation (PDFs) | Step 14 |

## Pain Points and Inefficiencies

### Critical Issues

1. **Manual Journal Entry Process**: Excel templates with manual data entry into SAP
   - **Impact**: High error rate including $50,000 account misclassification and $15,000 transposed digit variance; hundreds of line items manually keyed; inconsistent template quality with broken formulas; errors not caught until external audit
   - **Frequency**: Every month for 60 recurring + 20-30 non-recurring entries
   - **Affected Steps**: Steps 11, 12, 13

2. **Manual Account Reconciliation Process**: Entirely Excel-based with no workflow automation
   - **Impact**: Time-consuming manual comparison of 150 accounts; no real-time visibility into status; reconciliation issues can add 1-2 days to close timeline; documentation quality issues noted by auditors
   - **Frequency**: Every month for all 150 balance sheet accounts
   - **Affected Steps**: Steps 14, 15, 16, 17

3. **AP Three-Way Match Discrepancies**: 30-40% of invoices have matching issues
   - **Impact**: Each discrepancy requires research and resolution that can take days; forces accruals to meet close deadline; delays downstream processes
   - **Frequency**: 60-80 invoices per month (30-40% of ~200 total)
   - **Affected Steps**: Step 7

4. **Cross-Departmental Dependencies**: Close cannot proceed until AP, AR, Payroll, and Inventory complete their work
   - **Impact**: If any department is late (due to vacation, competing priorities), entire close timeline slips
   - **Frequency**: Every month
   - **Affected Steps**: Steps 4, 5, 6, 7, 8, 10

5. **Bank Reconciliation Timing Differences**: Transactions posted on different dates by bank vs. GL
   - **Impact**: Significant time spent tracking down differences (e.g., $23,000 difference took almost full day; wire transfers posted on different dates)
   - **Frequency**: Multiple times per month
   - **Affected Steps**: Steps 14, 15

### Inefficiencies

1. **Close Duration**: 8 business days vs. industry benchmark of 4-5 days for similar-sized companies
   - **Current State**: 8-day close process
   - **Impact**: 50 person-days total effort per month; staff accountants 100% dedicated for 8 days (32 person-days); Controller 60-70% time (4.8-5.6 person-days); limited capacity for value-added analysis and business partnering

2. **Manual Close Checklist**: Excel-based checklist with 80 line items requiring manual updates
   - **Current State**: Team members manually update checklist; Controller checks twice daily
   - **Impact**: Not automated; reactive problem identification; items slip through if updates forgotten; no real-time visibility

3. **Variance Analysis Process**: Manual Excel-based comparison requiring department head follow-up
   - **Current State**: Controller spends half day writing variance explanations and chasing department heads
   - **Impact**: Time-consuming; delays final reporting

4. **Documentation Quality**: Supporting schedules don't clearly tie to GL; missing signatures and dates
   - **Current State**: Manual documentation process under time pressure
   - **Impact**: Auditor findings; potential compliance issues; items skipped when rushing to meet deadline

5. **No Close Management Tool**: All workflows managed through Excel and email
   - **Current State**: Excel templates, email notifications, manual status tracking
   - **Impact**: No real-time dashboard; no automated data pulls from SAP; no workflow automation; Controller believes manual process costs more than close management software (BlackLine, FloQast) would cost

## Process Metrics
- **Total Steps**: 23
- **Number of Decision Points**: 5
- **Number of Actors**: 10 (roles/teams)
- **Identified Pain Points**: 9 (5 critical issues, 4 inefficiencies)
- **Manual Steps**: 18
- **Systems Involved**: 5
- **Current Close Duration**: 8 business days
- **Industry Benchmark**: 4-5 business days
- **Total Monthly Effort**: ~50 person-days
- **Number of Journal Entries**: 80-90 per month (60 recurring + 20-30 non-recurring)
- **Number of Accounts Reconciled**: 150
- **Number of Bank Accounts**: 12
- **Number of Invoices per Month**: ~200
- **Invoice Discrepancy Rate**: 30-40%
- **Close Checklist Items**: 80

## Notes and Observations

**Upcoming Changes**: 
- New HR system implementation next quarter will change payroll feed into GL
- Potential acquisition of small company would add new entity to consolidate
- Controller expressed concern about adding complexity without fixing underlying process issues

**What Works Well**:
- Daily standup calls during close week create accountability
- Recurring journal entry templates (despite quality issues) save time vs. creating from scratch
- Close calendar with published deadlines helps planning
- Team has improved at accruing based on estimates rather than waiting for perfect information

**Controls in Place**:
- Period locking in SAP prevents posting to closed months
- Segregation of duties: staff accountants prepare/enter (parked status), Controller approves/releases
- Two-signature requirement for bank reconciliations over $100,000
- Daily close checklist monitoring
- Daily standup calls during close week
- Controller review of all journal entries and reconciliations

**Resource Constraints**:
- Team is "stretched thin" with current workload
- Budget approval for close management software (BlackLine, FloQast) has been denied despite demonstrated need
- Limited capacity for analysis and value-added work due to manual close activities

**Quality Concerns**:
- Controller confident in final numbers but concerned about missing items due to time pressure
- Manual controls require significant effort
- Documentation quality issues noted by external auditors
- Errors have occurred that weren't caught until external audit

**Strategic Desire**:
- Controller wants team to spend more time on analysis, business partnering, and forward-looking work
- Recognizes need to modernize and automate to achieve this goal
- Views current project as opportunity to make business case for investment in tools and automation