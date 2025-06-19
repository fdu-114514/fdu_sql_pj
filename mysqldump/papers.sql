-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: literature_management_system
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `papers`
--

DROP TABLE IF EXISTS `papers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `papers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abstract` text COLLATE utf8mb4_unicode_ci,
  `publish_date` date DEFAULT NULL,
  `pdf_file_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `conference_journal_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_papers_publish_date` (`publish_date`),
  KEY `ix_papers_conference_journal_id` (`conference_journal_id`),
  KEY `ix_papers_title` (`title`),
  CONSTRAINT `papers_ibfk_1` FOREIGN KEY (`conference_journal_id`) REFERENCES `conference_journals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papers`
--

LOCK TABLES `papers` WRITE;
/*!40000 ALTER TABLE `papers` DISABLE KEYS */;
INSERT INTO `papers` VALUES (1,'Robust copula estimation for one-shot devices with correlated failure modes','This paper presents a robust method for estimating copula models to evaluate dependence between failure modes in one-shot devices-systems designed for single use and destroyed upon activation. Traditional approaches, such as maximum likelihood estimation (MLE), often produce unreliable results when faced with outliers or model misspecification. To overcome these limitations, we introduce a divergence-based estimation technique that enhances robustness and provides a more reliable characterization of the joint failure-time distribution. Extensive simulation studies confirm the robustness of the proposed method. Additionally, we illustrate its practical utility through the analysis of a real-world dataset.',NULL,'uploads/pdfs/69412d57-ced9-4ed5-bbb6-5251b98dce02.pdf',NULL),(2,'NEW CLASS OF TIME-PERIODIC SOLUTIONS TO THE 1D CUBIC WAVE EQUATION','In recent papers [FM25; FM24] we presented results suggesting the existence of a new class of time-periodic solutions to the defocusing cubic wave equation on a onedimensional interval with Dirichlet boundary conditions. Here we confirm these findings by rigorously constructing solutions from this class. The proof uses rational arithmetic computations to verify essential operator bounds.',NULL,'uploads/pdfs/277e5ac9-aef7-4106-b83e-ec8986853475.pdf',NULL),(3,'Rethinking Growth: An Extension of the Solow-Swan Model','The aggregate Cobb-Douglas production function stands as a central element in the renowned Solow-Swan model in economics, providing a crucial theoretical framework for comprehending the determinants of economic growth. This model not only guides policymakers and economists but also influences their decisions, fostering sustainable and inclusive development. In this study, we utilize a one-input version of a new generalization of the Cobb-Douglas production function proposed recently, thereby extending the Solow-Swan model to incorporate energy production as a factor. We offer a rationale for this extension and conduct a comprehensive analysis employing advanced mathematical tools to explore solutions to this new model. This approach allows us to effectively integrate environmental considerations related to energy production into economic growth strategies, fostering long-term sustainability.',NULL,'uploads/pdfs/dfb5532a-2469-43c1-b065-f1e1d9dbd53b.pdf',NULL),(4,'The Gittins Index: A Design Principle for Decision-Making Under Uncertainty','The Gittins index is a tool that optimally solves a variety of decision-making problems involving uncertainty, including multi-armed bandit problems, minimizing mean latency in queues, and search problems like the Pandora\'s box model. However, despite the above examples and later extensions thereof, the space of problems that the Gittins index can solve perfectly optimally is limited, and its definition is rather subtle compared to those of other multi-armed bandit algorithms. As a result, the Gittins index is often regarded as being primarily a concept of theoretical importance, rather than a practical tool for solving decision-making problems.The aim of this tutorial is to demonstrate that the Gittins index can be fruitfully applied to practical problems. We start by giving an example-driven introduction to the Gittins index, then walk through several examples of problems it solves-some optimally, some suboptimally but still with excellent performance. Two practical highlights in the latter category are applying the Gittins index to Bayesian optimization, and applying the Gittins index to minimizing tail latency in queues.',NULL,'uploads/pdfs/46a1502c-d53e-45f8-9d5a-ee539071bd35.pdf',NULL),(5,'FAST BAYESIAN OPTIMIZATION OF FUNCTION NETWORKS WITH PARTIAL EVALUATIONS','Bayesian optimization of function networks (BOFN) is a framework for optimizing expensive-toevaluate objective functions structured as networks, where some nodes\' outputs serve as inputs for others. Many real-world applications, such as manufacturing and drug discovery, involve function networks with additional properties -nodes that can be evaluated independently and incur varying costs. A recent BOFN variant, p-KGFN, leverages this structure and enables cost-aware partial evaluations, selectively querying only a subset of nodes at each iteration. p-KGFN reduces the number of expensive objective function evaluations needed but has a large computational overhead: choosing where to evaluate requires optimizing a nested Monte Carlo-based acquisition function for each node in the network. To address this, we propose an accelerated p-KGFN algorithm that reduces computational overhead with only a modest loss in query efficiency. Key to our approach is generation of node-specific candidate inputs for each node in the network via one inexpensive global Monte Carlo simulation. Numerical experiments show that our method maintains competitive query efficiency while achieving up to a 16× speedup over the original p-KGFN algorithm.',NULL,'uploads/pdfs/14f66499-188e-4c95-9bbd-1b267210d2dd.pdf',NULL),(6,'Limiting distributions of ratios of Binomial random variables','We consider the limiting distribution of the quantity X s /(X + Y ) r , where X and Y are two independent Binomial random variables with a common success probability and a number of trials n and m, respectively, and r, s are positive real numbers. Under several settings, we prove that this converges to a Normal distribution with a given mean and variance, and demonstrate these theoretical results through simulations.',NULL,'uploads/pdfs/bb196069-4e51-4994-937d-8dd68336d921.pdf',NULL);
/*!40000 ALTER TABLE `papers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-19 16:38:54
