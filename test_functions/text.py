text = "AI-based Telemetry Analysis and Root Cause Inference with PraxiPaaS A brief summary (1-2 pages) of the proposed work. Please address the following questions: 1. What is the student proposing to do? (e.g., identifying a specific need/problem and a method of investigating or approaching a solution.) 2. Are others working in this area? (A complete literature search is not necessary, but the proposer should reference any known work of a professor or developer who has done similar work, preferably explaining the connection to the proposed project. For example, a student seeking to expand an existing software library or open source project would reference that library or project.) 3. To whom is this work important, and why? 4. What will be needed from collaborators on the project to be successful? (e.g., access needed from Red Hat engineers, connections to developers working on an open source project, hardware in the MOC, etc.) In recent years, there has been increasing usage of cloud services, and companies opting to use cloud computing as their business model. One of the most popular types of cloud computing offerings is Platform as a service (PaaS). In PaaS, users, typically developers can leverage virtualized infrastructure without having to manage or worry about the underlying complexities directly. This enables developers to directly program and businesses to quickly deploy new applications. However, as some applications grow, so does the complexity of cloud architectures. Assessing the overall impact of each new component addition or the utilization of third party projects becomes challenging. In the case that there is a system fault or anomalous behavior, it is time-consuming and takes a high level of expertise to be able to diagnose the issue. Our suggested approach to address this issue involves employing the Software Bill of Materials (SBOM) alongside telemetry data extracted from containers. This combined approach aims to assess whether a change has the potential to cause a fault, providing administrators and users with a proactive strategy for issue identification and resolution. The objective of this project is to build upon the foundation of a package discovery framework named PraxiPaas and takes inspiration from a cloud-based cross-layer analytics system known as Tritium. PraxiPaaS is a framework designed to automatically inspect container packages in PaaS clusters. It utilizes package installation changes, employing file modifications during installations as package fingerprints to provide a SBOM. The work in Tritium synthesizes diverse data types to suggest potential causes for Service Level Objective (SLO) violations in microservice applications. Tritium takes event data to identify new version rollouts, constructs a topology graph for the cluster using tracing data to identify potentially affected services, and employs causal impact analysis on metric time-series to determine if the rollout is at fault. The proposed project aims to integrate these two frameworks, providing developers with a comprehensive tool for swift application diagnostics. This work is advantageous for developers, offering a diagnostic tool through the integration of PraxiPaaS and Tritium. It provides system administrators with proactive issue identification, ensuring improved system reliability. Businesses can also benefit from uninterrupted service delivery and reliability. For this project to be successful, access to telemetric data from clusters, advice on ML methods, and RHODES test cluster access would be needed. Another undergraduate, Rohan Kumar, will collaborate on this project, with mentoring provided by PhDstudent Zhongshun Zhang under the guidance of Professor Ayse Coskun. We will be building upon the foundation of PraxiPaas worked on by Zhonshun Zhang, and adopting a similar process to Tritium."
