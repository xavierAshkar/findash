

# 

# Design Document {#design-document}

## FinDash \- Financial Literacy Tool {#findash---financial-literacy-tool}

## Personal Software Engineering Project {#personal-software-engineering-project}

## Xavier Ashkar {#xavier-ashkar}

## **Contents** {#contents}

[Design Document](#design-document)

[FinDash \- Financial Literacy Tool](#findash---financial-literacy-tool)

[Personal Software Engineering Project](#personal-software-engineering-project)

[Xavier Ashkar](#xavier-ashkar)

[Contents](#contents)

[Overview](#overview)

[Definitions](#definitions)

[Introduction](#introduction)

[User Personas](#user-personas)

[Persona 1: Financial Beginner (Primary User)](#persona-1:-financial-beginner-\(primary-user\))

[Persona 2: Early Optimizer (Secondary User)](#persona-2:-early-optimizer-\(secondary-user\))

[System Concept Overview](#system-concept-overview)

[System Architecture](#system-architecture)

[Architectural Overview](#architectural-overview)

[Frontend Application Layer](#frontend-application-layer)

[Backend Application Layer](#backend-application-layer)

[Data Flow and State Ownership](#data-flow-and-state-ownership)

[External Data Integrations](#external-data-integrations)

[Architectural Principles](#architectural-principles)

[Non-functional Requirements](#non-functional-requirements)

[Accuracy & Consistency](#accuracy-&-consistency)

[Performance](#performance)

[Security & Privacy](#security-&-privacy)

[Reliability](#reliability)

[Usability](#usability)

[Maintainability](#maintainability)

[Functional Area Detail (Components and Modules)](#functional-area-detail-\(components-and-modules\))

[Account Management Module](#account-management-module)

[Transaction Management Module](#transaction-management-module)

[Cash Flow Aggregation Module](#cash-flow-aggregation-module)

[Short-Term Goals Module](#short-term-goals-module)

[Long-Term Goals Module](#long-term-goals-module)

[Gamification & Feedback Module](#gamification-&-feedback-module)

## **Overview** {#overview}

The scope of this document is to describe the system-level and detailed design of FinDash, a beginner-focused financial literacy platform. The topics covered include the project’s architecture, major functional areas, UI/UX design, system components, technology choices, dependencies, testing strategy, anticipated risks, and development milestones. This document focuses specifically on how the system is structured, organized, and intended to evolve, rather than on low-level implementation details.

This document does not describe full source code, finalized UI styling, or completed backend infrastructure. These elements will be implemented and iterated upon during development based on the architectural and design decisions outlined here.

	The purpose of this design document is to establish a clear engineering and product blueprint for FinDash. It defines the guiding principles, system responsibilities, workflows, and constraints that will shape development. By doing so, this document serves as a stable reference point, ensuring that design decisions remain intentional and consistent throughout the project lifecycle.

The intended audience of this document includes the project author, potential collaborators, future contributors, and external reviewers who wish to understand the system’s design and reasoning. The document assumes a general knowledge of software engineering but does not require prior familiarity with financial systems or budgeting tools.

## **Definitions** {#definitions}

**Transaction** – A single financial event representing either income or an expense, associated with an amount, category, and date.

**Cash Flow** – The relationship between money entering and leaving a user’s finances over a given period, typically evaluated monthly.  
**Monthly Summary** – An aggregated view of all transactions within a given month, including total income, total expenses, and net remaining funds.  
**Monthly Goal** – A short-term financial target defined for a specific month, such as limiting spending or achieving a savings threshold.  
**Long-Term Goal** – A persistent financial objective that spans multiple months, such as building an emergency fund or paying down debt.  
**Financial Literacy** – The ability to understand and reason about personal financial concepts such as budgeting, saving, debt, and long-term planning.

## **Introduction** {#introduction}

Managing personal finances is not merely a problem of tracking numbers, but one of understanding behavior, intent, and progress over time. Many individuals entering financial independence struggle not because they lack access to data, but because they lack a clear framework for interpreting it. Existing financial tools often prioritize automation, optimization, and advanced analytics, assuming users already possess foundational financial literacy. For beginners, this complexity can obscure essential insights and discourage sustained engagement, which is critical for achieving long-term financial stability.

While some platforms automate nearly all aspects of financial tracking, this approach can distance users from the underlying financial reality they are meant to understand. Conversely, fully manual tracking methods such as spreadsheets or handwritten logs require sustained effort and discipline, making them difficult to maintain consistently. Neither extreme adequately supports beginners who need guidance, clarity, and motivation as they develop financial habits.

FinDash is designed to address this gap by combining automated data aggregation with intentional user interaction. The platform emphasizes financial awareness rather than raw automation, allowing users to observe cash flow patterns, understand spending behavior, and track progress toward meaningful goals. Instead of presenting financial data as isolated metrics, FinDash organizes information around user-defined objectives, helping users understand how daily financial activity connects to both short-term actions and long-term outcomes.

At a high level, FinDash introduces users to their finances through a structured onboarding process in which a primary long-term financial goal is established. This goal serves as an anchor for the user’s experience. Based on the user’s current financial state, including cash flow, savings, debt, and net worth, the system recommends achievable short-term goals designed to move the user incrementally toward their long-term objective. Short-term and long-term goals remain user-configurable, allowing the experience to adapt as financial circumstances evolve.

Through clear visualizations, goal-driven feedback, and lightweight gamification, FinDash transforms financial literacy from an abstract responsibility into an interactive and approachable process. The system is designed to make progress visible, reinforce positive behavior, and support sustainable financial habit formation without overwhelming the user.

## **User Personas** {#user-personas}

#### **Persona 1: Financial Beginner (Primary User)** {#persona-1:-financial-beginner-(primary-user)}

**Profile:**

* Age: 18-25  
* Status: Student or early-career professional  
* Income: Inconsistent or entry-level  
* Financial tools used: None or basic banking apps

**Pain Points:** 

* Feels overwhelmed by financial terminology  
* Unsure where their money is going each month  
* Difficulty connecting daily spending to long-term goals  
* Intimidated by “advanced” budgeting tools

**Goals:**

* Understand monthly cash flow  
* Build basic financial habits  
* Work toward a clear long-term objective (e.g., emergency fund)

**Needs from FinDash:**

* Simple explanations and visuals  
* Minimal required setup  
* Clear feedback on progress  
* Motivation to stay engaged without guilt or pressure

#### **Persona 2: Early Optimizer (Secondary User)** {#persona-2:-early-optimizer-(secondary-user)}

**Profile:**

* Age: 22-30  
* Status: Full-time employed  
* Income: Consistent  
* Financial tools used: Competitors, now disengaged

**Pain Points:** 

* Tools feel overly complex  
* Too many metrics without a clear direction  
* Lacks motivation to maintain tracking

**Goals:**

* Maintain awareness without micromanagement  
* Track progress toward one major goal  
* Reduce cognitive load

**Needs from FinDash**

* Goal-driven insights  
* Minimal configuration  
* Clear success states

## **System Concept Overview** {#system-concept-overview}

	FinDash proposes a goal-oriented financial literacy platform centered around three core functional areas: **Cash Flow Awareness**, **Short-Term Financial Goals**, and **Long-Term Financial Objectives**. These components work together to create a feedback-driven system that helps users understand their finances, take intentional action, and measure progress over time.

The foundation of the platform is the **Cash Flow** section. This area provides users with a clear view of money entering and leaving their accounts over configurable time periods, typically monthly. Users can explore historical data across months and years to identify trends in income, spending, and category distribution. Financial data may be sourced through connected financial accounts or user input, and is presented through clear, accessible visualizations designed to emphasize understanding rather than dense analysis.

Building on this foundation, FinDash enables users to define **Short-Term Goals** related to saving and spending. These goals are evaluated continuously using cash flow data and, when available, linked account information. The system provides timely feedback on goal progress, allowing users to observe how everyday financial decisions influence their ability to meet short-term objectives.

At the core of the user experience is the **Long-Term Goals** system. During onboarding, users are encouraged to define a primary long-term financial goal, such as building an emergency fund, paying down debt, or reaching a net worth milestone. While multiple long-term goals may be configured, the system encourages focus on a single primary objective to reduce cognitive overload and maintain clarity. This long-term goal serves as the guiding reference point for the application.

Based on the user’s current financial state, including cash flow, savings, debt, and net worth, FinDash recommends a set of short-term goals designed to move the user steadily toward their long-term objective. These recommendations adapt over time as the user’s financial situation evolves.

Progress toward both short-term and long-term goals is presented visually and reinforced through lightweight gamification elements, such as progress indicators, milestone achievements, and clear completion states. The intent is not to trivialize financial responsibility, but to make progress tangible and motivating for beginners.

By structuring financial data around goals rather than isolated metrics, FinDash enables users to understand *why* financial behaviors matter and *how* small, consistent actions contribute to meaningful outcomes. This approach prioritizes education, engagement, and long-term habit formation over optimization or complexity.

## **System Architecture** {#system-architecture}

The FinDash system is designed using a layered, goal-driven architecture that separates data aggregation, business logic, and user-facing presentation. This structure ensures clarity of responsibility, maintainability, and the ability to evolve individual system components without destabilizing the overall platform. At a high level, the system consists of three primary layers: the **Frontend Application Layer**, the **Backend Application Layer**, and **External Data Integrations**.

#### **Architectural Overview** {#architectural-overview}

FinDash follows a client–server architecture in which the backend serves as the authoritative source of truth for financial data, goal evaluation, and recommendation logic, while the frontend focuses on visualization, interaction, and feedback. All user-facing state is derived from backend-provided data to ensure consistency and correctness across sessions and devices.  
The architecture is designed to support a feedback loop in which financial data informs goal evaluation, goal progress informs user feedback, and user actions continuously update the underlying financial state.

#### **Frontend Application Layer** {#frontend-application-layer}

The frontend application is responsible for presenting financial information in a clear, approachable, and engaging manner. It renders dashboards, cash flow visualizations, goal progress indicators, and educational feedback while handling user interaction, navigation, and micro-interactions.

Key responsibilities of the frontend include:

* Displaying cash flow summaries and historical trends  
* Visualizing short-term and long-term goal progress  
* Providing interactive controls for goal configuration and time-period selection  
* Rendering gamified feedback elements such as progress indicators and milestones  
* Managing transient UI state (e.g., selected month, expanded views, animations)

The frontend does not perform authoritative financial calculations or goal evaluation logic. Instead, it consumes structured data from the backend and presents it in a form optimized for comprehension and engagement.

#### **Backend Application Layer** {#backend-application-layer}

	The backend application serves as the core logic and data management layer of FinDash. It is responsible for storing financial data, evaluating goals, generating recommendations, and enforcing consistency across the system.

Key responsibilities of the backend include:

* Persisting user financial data, including transactions, categories, and summaries  
* Aggregating cash flow data across configurable time periods  
* Evaluating short-term and long-term goal progress  
* Generating recommended short-term goals based on the user’s long-term objective and current financial state  
* Managing user authentication, authorization, and data security  
* Serving structured API responses to the frontend

All calculations related to cash flow aggregation, goal completion, and progress tracking are performed on the backend to ensure correctness and reproducibility.

The backend maintains an Account abstraction representing individual financial accounts such as checking accounts, savings accounts, credit cards, and cash holdings. Accounts act as a normalization layer between external data integrations and internal financial analysis. All transactions are associated with a specific account, allowing consistent inclusion rules, filtering, and aggregation when generating cash flow summaries or evaluating goals.

#### **Data Flow and State Ownership** {#data-flow-and-state-ownership}

	Financial data flows through the system in a unidirectional manner to maintain clarity and traceability:

1. Transaction data is ingested from external integrations or user input.  
2. The backend aggregates transaction data into cash flow summaries.  
3. Cash flow summaries are used to evaluate goal progress and generate recommendations.  
4. The frontend retrieves processed data and renders visualizations and feedback.  
5. User interactions (e.g., goal updates, configuration changes) are sent back to the backend for validation and persistence.

This unidirectional data flow ensures that all derived state originates from a single authoritative source and prevents inconsistencies between displayed data and stored data.

![][image1]  
**Figure 1\. High-level Financial Data Flow & Goal Evaluation Pipeline**

#### **External Data Integrations** {#external-data-integrations}

	FinDash integrates with external financial data providers, such as Plaid, to retrieve transaction and account information when users choose to connect their accounts. These integrations are treated as **supporting data sources**, not primary system controllers.

External integrations are used to:

* Reduce manual data entry  
* Improve the accuracy of cash flow data  
* Provide timely updates on the financial state

All externally sourced data is validated and normalized by the backend before being incorporated into the system’s data model. Users retain the ability to interact with and interpret their financial data regardless of whether external integrations are enabled.

#### **Architectural Principles** {#architectural-principles}

The system architecture is guided by the following principles:

* **Backend authority**: All financial logic and state evaluation occur on the backend.  
* **Frontend clarity**: The frontend exists to interpret and communicate data, not to define it.  
* **Goal-first design**: Architectural decisions prioritize goal tracking and progress feedback.  
* **Modularity**: Components are designed to evolve independently as features expand.  
* **Maintainability**: Clear separation of concerns minimizes coupling and reduces complexity.

This architecture provides a stable foundation for future feature expansion, including additional goal types, educational modules, or enhanced visualization techniques, without requiring fundamental restructuring of the system.

## **Non-functional Requirements** {#non-functional-requirements}

#### **Accuracy & Consistency** {#accuracy-&-consistency}

* All financial calculations (cash flow, goal progress) must be deterministic and reproducible.  
* Backend is the authoritative source of truth for all derived financial data.  
* Frontend must only display backend-evaluated values.

#### **Performance** {#performance}

* Monthly cash flow views should load within **500ms** under normal conditions.  
* Goal progress updates should reflect new data within a single refresh cycle.  
* External data sync delays must not block UI responsiveness.

#### **Security & Privacy** {#security-&-privacy}

* User financial data must be isolated per account.  
* All sensitive data must be transmitted over HTTPS.  
* External integrations must use secure token-based authentication.  
* Secrets and credentials must never be exposed to the frontend.

#### **Reliability** {#reliability}

* The system must gracefully handle missing or delayed external data.  
* Partial data availability must not break core views.  
* Failures in external integrations must degrade functionality, not crash the system.

#### **Usability** {#usability}

* Core workflows must be understandable without prior financial knowledge.  
* Users should be able to complete onboarding in under **5 minutes**.  
* Progress toward goals must be visually clear without requiring interpretation.

#### **Maintainability** {#maintainability}

* Backend logic must be modular and testable.  
* Frontend components should remain loosely coupled to data sources.  
* The system must support incremental feature expansion without structural rewrites.

## **Functional Area Detail (Components and Modules)** {#functional-area-detail-(components-and-modules)}

The FinDash backend is organized into a set of clearly defined functional modules, each responsible for a specific domain within the system. This modular structure enforces separation of concerns, improves maintainability, and allows individual components to evolve independently as the platform grows.

Each module is defined by its purpose, core responsibilities, inputs, outputs, and explicit scope. Together, these modules form a linear processing pipeline that supports the flow of financial data from ingestion through aggregation and goal evaluation, as described in the System Architecture section.

#### 

#### **Account Management Module** {#account-management-module}

**Purpose**  
The Account Management Module defines and manages the financial accounts associated with a user. It serves as the normalization layer between external data sources and internal financial analysis, ensuring consistent handling of different account types.

**Responsibilities**

* Store and manage user financial accounts, including checking accounts, savings accounts, credit cards, and cash holdings  
* Normalize account data from external integrations and manual input  
* Maintain account metadata such as account type, institution, status, and user-defined labels  
* Control inclusion and exclusion rules for downstream financial analysis  
* Provide account context for transactions and aggregation logic

**Inputs**

* Account data from external financial integrations (e.g., Plaid)  
* User-initiated account configuration changes (e.g., renaming, inclusion toggles)

**Outputs**

* Normalized account objects used by the Transaction and Cash Flow modules  
* Account metadata for display and filtering in the frontend

**Non-Responsibilities**

* Transaction ingestion or categorization  
* Cash flow aggregation  
* Goal evaluation or recommendation logic

#### **Transaction Management Module** {#transaction-management-module}

**Purpose**  
The Transaction Management Module is responsible for ingesting, storing, and managing individual financial transactions. It represents the system’s authoritative record of financial activity.

**Responsibilities**

* Ingest transaction data from external integrations and manual user input  
* Associate each transaction with a specific account  
* Store transaction attributes, including amount, date, description, and category  
* Support transaction filtering and querying by time period, account, or category  
* Preserve transaction history to support accurate financial analysis

**Inputs**

* Transaction data from external integrations  
* User-submitted transactions or category adjustments

**Outputs**

* Structured transaction records consumed by the Cash Flow Aggregation Module  
* Transaction data for frontend display and inspection

**Non-Responsibilities**

* Cash flow aggregation  
* Goal evaluation  
* Long-term data interpretation


#### **Cash Flow Aggregation Module** {#cash-flow-aggregation-module}

**Purpose**  
The Cash Flow Aggregation Module transforms raw transaction data into meaningful summaries that describe patterns of income and spending over time.

**Responsibilities**

* Aggregate transactions across accounts and time periods  
* Compute inflows, outflows, and net cash flow  
* Apply account inclusion rules during aggregation  
* Generate category-level spending breakdowns  
* Produce time-based summaries for frontend visualization

**Inputs**

* Transaction records  
* Account inclusion and configuration data

**Outputs**

* Cash flow summaries and derived metrics  
* Aggregated data used by goal evaluation and visualization layers

**Non-Responsibilities**

* Transaction ingestion or modification  
* Goal recommendation logic  
* UI presentation


#### **Short-Term Goals Module** {#short-term-goals-module}

**Purpose**  
The Short-Term Goals Module manages actionable financial targets designed to guide user behavior over short time horizons, typically monthly, toward a long-term goal.

**Responsibilities**

* Store and manage short-term financial goals  
* Evaluate goal progress using cash flow summaries  
* Determine goal completion states  
* Provide progress metrics for visualization and feedback  
* Support system-recommended short-term goals based on user context

**Inputs**

* Cash flow summaries  
* User-defined goal parameters  
* Long-term goal context

**Outputs**

* Short-term goal progress evaluations  
* Goal status updates and completion signals

**Non-Responsibilities**

* Long-term planning logic  
* Transaction aggregation  
* Financial data ingestion


#### **Long-Term Goals Module** {#long-term-goals-module}

**Purpose**  
The Long-Term Goals Module represents the user’s primary financial objectives and provides direction for the system’s recommendation and feedback mechanisms.

**Responsibilities**

* Store and manage long-term financial goals  
* Track progress toward long-term objectives using derived financial metrics  
* Provide contextual information for short-term goal recommendations  
* Support updates and goal adjustments as user circumstances change

**Inputs**

* Aggregated financial metrics  
* User-defined long-term goal parameters

**Outputs**

* Long-term goal progress metrics  
* Context for short-term goal recommendation logic

**Non-Responsibilities**

* Short-term goal execution  
* Cash flow aggregation  
* UI rendering

#### **Gamification & Feedback Module** {#gamification-&-feedback-module}

**Purpose**  
The Gamification & Feedback Module translates financial progress into visible, motivating signals that encourage sustained engagement.

**Responsibilities**

* Interpret goal progress into milestone events  
* Generate completion acknowledgments and progress indicators  
* Provide structured feedback signals for frontend visualization

**Inputs**

* Short-term and long-term goal progress data

**Outputs**

* Feedback events and progress markers consumed by the frontend

**Non-Responsibilities**

* Financial calculations  
* Goal evaluation  
* Data aggregation

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnAAAAAgCAYAAACSAkV9AAAWu0lEQVR4Xu2dhZPkNhPFv/8pzMzMzIwVujAnF2ZmZrjwhTm5cC54Ybjkwsyc+eqnqjfpbVte2zuztzPbr6rLGlmWrHar9QT2/O+XX37phISEhISEhISEDI78z0eEhISEhISEhIRMbOkSuJ9//rnz448/dqZOndqZMmVKSMhcl6OPPrrz5ZdfFoxW8tVXXxXikC+++KIQh/z000/Jxg899NBCWcMic+bMyeolF49eaP8+Hvn6668706ZNK5QzmWX69OmtdenjkM8//7wze/bsQjnDJD/88EPSja87kmvjufQIujz44IML5YT0Rp577rmsvfIsfZzk22+/LcQhn332WWfWrFmFckKaycyZM5Mupdcugfvmm28KiUNC5rbgpL0zkLz33nuFOOTdd98txCGQG5//MMott9xSqHuVvnDUOad80EEHFfIPydtlTpeQug8//LAQj1xyySWF/IdRIKq+7kiVXfo4BF2GXfZfHnnkkYLuEQbIZeSa5/Lxxx8X4pHTTjutkH9IOznxxBO7eu0SODUIOrlAYCJAhOutt94qOIQ2cuCBB6b8vvvuO1/UUODvv//uNnJf97ZCXldeeaUvalLj5JNP7rmO999//86///7rixoKyC4PP/zwQt3bCP6A/CDKgf7gmGOO6ey7774F3bcVnhcrH8Nq4+MBdKfVI+m1S+Dk+AOBiQRs8s477yw4hDaiTmSY8cADD/SMXHz//fcpr3/++ccXM+mBXtCP11kbIa8nnnjCFzFUUP/i695GLrroouir+gxm2Hr1vF5++eWU1zvvvOOLCTTEm2++GQQuMDgIAtcMQeDGB0HgmiEI3GAhCNzERBC4wEAhCFwzBIEbHwSBa4YgcIOFIHATE0HgAgOFIHDNEARufBAErhmCwA0WgsBNTASBCwwUcgSON54efPDBQjwCifFxsvHJTOBy+uKt3U8//bQQHwQujxyBy+mSDvHxxx8vxCOTncA9/PDDhTgk93ZqELj+o4rAvfbaa+lFMB/PNc8++2whPghc7xAELjBQyBE4L7yRRtrca+yy8clM4Lwccsghnf32268QLwkCl0eOwHl56KGHRn0ek53AeSHdOeecU4iXBIHrP6oInJebbrqpc8ABBxTiJUHgeocgcIGBAjZZh8BZG86N3DkXBO4/ueeeeyo7yyBweaCXOgSOj9SStqqD43wQuP+ET6pU2WUQuP6jCYHjw7Kk5TNN/hwSBK53aEXgFlxwwc4888wzQnLA2f/5558+umegbBqwcOmll3bvad111+0888wzJnU5uL8mnZLqa8taaqml0ocOAd/Qq9LJ0ksv3TnssMN8dLqGa4WFFlooEYwyHXPPxJ177rkj4nsNyrDfV1KdewW+ZSP7eP3110fNG5usS+AQOkquueyyywrniK9D4KT/J5980p8aN/DtrDbtqAmBQ/hyOun55pP/OGcVgVt88cW7epLMN998Ptm4An399ddfKVzWhnoJ9FKHwEnkXz/55JPSczkCx1aBNddcM9WFGdOyZzEa6upBPga58MILa19XB6q/r3tO7r777pT+9NNPL5wbjcDdeuut6d4XXnjhzgcffJDixmoP6KbqG2Zt2moTsPyuNobfbAOuf+qpp3x0KZoQOISPNOsZ+3/CKSNw119//ZieRxP0m5MAPq4rG2v7ndE6+mhN4JBdd921KzncdttttW6kLci7jMDh5CBAhOlcqtDEkPk7pyWXXDKFKWv++edP9V955ZW79RyNwLEvpgxcYwmc8pAh0BkLW2+9dYobdAL30UcfjchvscUW61x33XUmxUhgk00IHEJHx3V+Jo64JgSul/VuirYdaFMCh9x1113pGmY+LImrInD77LNPageLLLJIuk/Cu+++u082ruA+Nt988xSms6Dj6BfQSxMCR6cmH+vPEZcjcLLDnXfeOR3xP01R146WW265zsYbb5z+Jqyt/eWQq3uVyC7PP//8EfFVBG6zzTZL933cccd1VlhhhW4dxtqeufaVV17x0V2MJe/RsOGGG6b8t99++zRxQLjNx7W5rm6/15TAIZqJ89fNbQLH34L1s6zjjz8+5Y/vWXHFFVOYf11pijr32JrALbPMMj46EaZff/21G6bjXGCBBdKN8BtQEcI4nhdffDHFrbXWWulr5oyQzjvvvHT+999/T0euF1566aUUh7ABG5B3GYETmBXj9/vvv59+o1DKpiyAg+I8dbriiitSHGSMNJAJj2WXXTbNTgDKsuSQPPbaa68RBO7ee+9N8dRDoz/qi0MEdJKce+yxx9I1InAaYQGOCJ2joDgROJYXKAfdyFgIsweMunIOMILXs1AadAC23HLLdC+LLrpod4RCGTkC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>