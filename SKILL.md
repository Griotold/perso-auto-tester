---
name: perso-qa-planner
description: Creates phase-based feature plans for PERSO Auto Tester QA automation project. Use when planning features, organizing work, breaking down tasks, creating roadmaps, or structuring development strategy. Keywords: plan, planning, phases, breakdown, strategy, roadmap, organize, structure, outline, perso, qa, automation.
---

# PERSO QA Feature Planner

## Purpose
Generate structured, phase-based plans for PERSO Auto Tester where:
- Each phase delivers complete, runnable functionality
- Quality gates enforce validation before proceeding
- Developer manually tests and provides feedback
- Progress tracked via markdown checkboxes
- Each phase is 1-4 hours maximum

## Planning Workflow

### Step 1: Requirements Analysis
1. Read relevant files to understand codebase architecture
2. Identify dependencies and integration points (Playwright, FastAPI, WebSocket)
3. Assess complexity and risks
4. Determine appropriate scope (small/medium/large)

### Step 2: Phase Breakdown
Break feature into 3-7 phases where each phase:
- Delivers working, testable functionality
- Takes 1-4 hours maximum
- Can be manually tested by developer
- Can be rolled back independently
- Has clear success criteria

**Phase Structure**:
- Phase Name: Clear deliverable
- Goal: What working functionality this produces
- Tasks (ordered by workflow):
  1. **Planning & Design**: Define components and architecture
  2. **Implementation**: Write code
  3. **Developer Manual Testing**: Developer tests and provides feedback
  4. **Bug Fixes & Improvements**: Address developer feedback
  5. **Code Review & Refinement**: Improve code quality
- Quality Gate: Developer approval + code quality validation
- Dependencies: What must exist before starting

### Step 3: Plan Document Creation
Use plan-template.md to generate: `docs/plans/PLAN_<feature-name>.md`

Include:
- Overview and objectives
- Architecture decisions with rationale
- Complete phase breakdown with checkboxes
- Quality gate checklists (developer approval required)
- Risk assessment table
- Rollback strategy per phase
- Progress tracking section
- Notes & learnings area

### Step 4: User Approval
**CRITICAL**: Use AskUserQuestion to get explicit approval before proceeding.

Ask:
- "Does this phase breakdown make sense for PERSO Auto Tester?"
- "Any concerns about the proposed approach?"
- "Should I proceed with creating the plan document?"

Only create plan document after user confirms approval.

### Step 5: Document Generation
1. Create `docs/plans/` directory if not exists
2. Generate plan document with all checkboxes unchecked
3. Add clear instructions in header about quality gates
4. Inform user of plan location and next steps

## Quality Gate Standards

Each phase MUST validate these items before proceeding to next phase:

**Developer Approval** (CRITICAL):
- [ ] Manual testing complete
- [ ] No critical issues found
- [ ] Developer feedback addressed
- [ ] Developer sign-off received

**Build & Code Quality**:
- [ ] Project runs without errors
- [ ] Linting passes with no errors (`ruff check .`)
- [ ] Code formatting consistent (`black --check .`)
- [ ] Type checking passes (`mypy .`)

**Functionality**:
- [ ] Manual testing confirms feature works
- [ ] No regressions in existing functionality
- [ ] Edge cases tested

**Security & Performance**:
- [ ] No new security vulnerabilities
- [ ] No performance degradation
- [ ] Resource usage acceptable (CPU/Memory)

**Documentation**:
- [ ] Code comments updated
- [ ] Documentation reflects changes

## Progress Tracking Protocol

Add this to plan document header:
```markdown
**CRITICAL INSTRUCTIONS**: After completing each phase:
1. ✅ Check off completed task checkboxes
2. 🧪 Perform manual testing and get developer approval
3. ⚠️ Verify ALL quality gate items pass
4. 📅 Update "Last Updated" date
5. 📝 Document learnings in Notes section
6. ➡️ Only then proceed to next phase

⛔ DO NOT skip quality gates or proceed with failing checks
```

## Phase Sizing Guidelines

**Small Scope** (2-3 phases, 3-6 hours total):
- Single component or simple feature
- Minimal dependencies
- Clear requirements
- Example: Add logging to existing test, create notification helper

**Medium Scope** (4-5 phases, 8-15 hours total):
- Multiple components or moderate feature
- Some integration complexity
- Example: Teams notification system, scheduler automation

**Large Scope** (6-7 phases, 15-25 hours total):
- Complex feature spanning multiple areas
- Significant architectural impact
- Multiple integrations
- Example: Electron desktop app, environment config system with security

## Risk Assessment

Identify and document:
- **Technical Risks**: Playwright flakiness, timing issues, browser compatibility
- **Dependency Risks**: External library updates, Teams webhook changes
- **Timeline Risks**: Complexity unknowns, blocking dependencies
- **Quality Risks**: E2E test coverage gaps, regression potential

For each risk, specify:
- Probability: Low/Medium/High
- Impact: Low/Medium/High
- Mitigation Strategy: Specific action steps

## Rollback Strategy

For each phase, document how to revert changes if issues arise.
Consider:
- What code changes need to be undone
- Configuration changes to restore
- Dependencies to remove
- Manual cleanup steps (e.g., delete scheduled jobs)

## Project-Specific Guidelines

### Technology Stack
- **Backend**: Python 3.12, FastAPI, Playwright
- **Frontend**: HTML, Vanilla JavaScript, WebSocket
- **Testing**: Manual E2E testing (developer-driven)
- **Deployment**: DigitalOcean App Platform

### Project Structure
```
perso-auto-tester/
├── api/              # FastAPI routes
│   ├── main.py
│   └── routers/
├── tasks/            # Test scripts (login, upload, translate)
├── utils/            # Helper modules (browser, logger, config)
├── templates/        # HTML templates
└── docs/plans/       # Implementation plans
```

### Code Quality Commands
```bash
# Linting
pdm run ruff check .

# Formatting
pdm run black .

# Type Checking
pdm run mypy .

# Run server
pdm run dev

# Run local E2E test (with browser visible)
pdm run test_login
pdm run test_upload
pdm run test_translate
```

### Development Workflow
1. **AI Implementation**: Write code based on phase tasks
2. **Code Quality**: Run ruff, black, mypy
3. **Developer Testing**: Developer runs manual E2E tests
4. **Feedback Loop**: Developer provides feedback, AI fixes issues
5. **Quality Gate**: All checks pass + developer approval
6. **Next Phase**: Proceed to next phase

### Key Constraints
- **No Automated E2E Tests**: Developer performs manual browser testing
- **WebSocket Real-time Logs**: Ensure log callbacks work correctly
- **Headless/Headed Modes**: Code must work in both modes
- **Resource Usage**: Monitor CPU/Memory (limited server resources)
- **Queue System**: Consider concurrent execution limits

## Developer Testing Guidelines

### For Each Phase
Provide clear testing instructions:
- **What to test**: Specific user scenario
- **Expected behavior**: What should happen
- **Test steps**: Numbered step-by-step instructions
- **Edge cases**: Specific edge cases to check
- **Known limitations**: Current constraints

### Example Testing Request Format
```markdown
**👤 Developer Manual Testing**
- [ ] **Task X.Y**: Request developer testing
  - **What to test**: Teams notification after test completion
  - **Expected behavior**: Message appears in #qa-alerts channel
  - **Test steps**:
    1. Run: `pdm run test_translate`
    2. Wait for test completion (3-5 minutes)
    3. Check Teams #qa-alerts channel
    4. Verify message format
  - **Edge cases to check**:
    - Invalid webhook URL handling
    - Network timeout handling
  - **Known limitations**: Currently only sends on success
  
  **Developer feedback**: [Developer fills after testing]
  - ✅ Works / ❌ Issues found
  - Issues: [List problems]
  - Suggestions: [Improvements]
```

## Common Patterns for PERSO Auto Tester

### Pattern 1: Adding New Test Step
**Phases**:
1. Define test logic and integration points
2. Implement test function with logging callbacks
3. Add WebSocket endpoint integration
4. Developer manual testing + feedback
5. Polish and error handling

### Pattern 2: External Integration
**Phases**:
1. Research API/service and design integration
2. Implement integration module (utils/)
3. Add to existing test workflow
4. Developer manual testing + feedback
5. Error handling and retry logic

### Pattern 3: UI Enhancement
**Phases**:
1. Design HTML/CSS changes
2. Implement frontend changes
3. Add backend endpoint if needed
4. Developer manual testing + feedback
5. Cross-browser compatibility check

## Supporting Files Reference
- [plan-template.md](plan-template.md) - Complete plan document template