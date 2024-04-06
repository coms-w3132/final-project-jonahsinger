# COMS W3132 Individual Project

## Author
Jonah Singer jrs2338@columbia.edu

## Project Title
Stock Market Predictor

## Project Description

I am interested in the intersection of computer science and finance so I would love to gain experience using Python to make financial models that can suggest stock trades. Trading stocks based on advanced statistical models and sophisticated data analysis in attempts to beat the stock market is a multi-billion dollar industry. This being the case, It is obvious that I will not be able to create algorithms that rival those of large companies. Nevertheless, I would like to implement a few algorithms and back-test them to see if I can generate any meaningful insights into the stock market and most importantly to gain experience working with financial data and testing algorithms. Before I am able to write algorithms I need to get data from the stock market I plan to do this with the yahoo finance yfinance package. I will also need to make a backtesting framework that can receive trades and simulate the resulting returns they would have generated, This framework will also use the pricing data from yahoo finance it will have methods to buy and sell and keep track of trades and returns. I want to implement and test three types of algorithms. The first algorithm will be a linear regression algorithm that takes linear regressions of the prices of many stocks over some period of time, X, and uses the linear regression to choose the stocks that are trending up to buy. I want to test this strategy using different time intervals, X, and also try using the linear regression to short stocks that are trending down. The second algorithm will be a mean reversion algorithm that will calculate the moving average of stocks over some time interval, Y, and buy stocks when the price is some amount, Z, below the moving average. I will experiment with testing different parameters Y and Z. I would also like to test in the algorithm shorting stocks when the price is some amount above the moving average. For the third algorithm, I want to try and gain experience using machine learning. I want to use the tensor flow library to make a neural network to suggest trades to make. The neural network will be trained with the price data of certain stocks. The hope is that what it learns from its training will be transferable to other stocks and for the future as well. The only real way to test this would be to have the algorithm trade what it has learned and to wait and see how the trades do in the future (this is not very practical for testing). I will use appropriate data structures to try and keep the running time of the algorithms as low as possible.

## Timeline

*To track progress on the project, we will use the following intermediate milestones for your overall project. Each milestone will be marked with a tag in the git repository, and we will check progress and provide feedback at key milestones.*

| Date               | Milestone                                                                                              | Deliverables                | Git tag    |
|--------------------|--------------------------------------------------------------------------------------------------------|-----------------------------|------------|
| **March&nbsp;29**  | Submit project description                                                                             | README.md                   | proposal   |
| **April&nbsp;5**   | Update project scope/direction based on instructor/TA feedback                                         | README.md                   | approved   |
| **April&nbsp;12**  | Basic project structure with empty functions/classes (incomplete implementation), architecture diagram | Source code, comments, docs | milestone1 |
| **April&nbsp;19**  | Progress on implementation (define your own goals)                                                     | Source code, unit tests     | milestone2 |
| **April&nbsp;26**  | Completely (or partially) finished implementation                                                      | Source code, documentation  | milestone3 |
| **May&nbsp;10**    | Final touches (conclusion, documentation, testing, etc.)                                               | Conclusion (README.md)      | conclusion |

*The column Deliverables lists deliverable suggestions, but you can choose your own, depending on the type of your project.*

## Requirements, Features and User Stories
*List the key requirements or features of your project. For each feature, provide a user story or a simple scenario explaining how the feature will be used. You don't have to get this section right the first time. Your understanding of the problem and requirements will improve as you work on your project. It is okay (and desirable) to come back to this section and revise it as you learn more about the problem you are trying to solve. The first version of this section should reflect your understanding of your problem at the beginning of the project.*
*Also list any required hardware, software, on online services you will need. In specific cases, we might be able to lend you hardware or obtain online services. Please email the instructor for more details.*

This project will have three different algorithms to trade in the stock market. The hope is that through the prosses of making and testing these algorithms I will find some meaningful insights into the stock market. In the end it is possible that a user could use these algorithms to generate meaningful trading advice.

## Technical Specification
*Detail the main algorithms, libraries, and technologies you plan to use. Explain your choice of technology and how it supports your project goals.*

Also in the project description:
The first algorithm will be a linear regression algorithm that takes linear regressions of the prices of many stocks over some period of time, X, and uses the linear regression to choose the stocks that are trending up to buy. I want to test this strategy using different time intervals, X, and also try using the linear regression to short stocks that are trending down. The second algorithm will be a mean reversion algorithm that will calculate the moving average of stocks over some time interval, Y, and buy stocks when the price is some amount, Z, below the moving average. I will experiment with testing different parameters Y and Z. I would also like to test in the algorithm shorting stocks when the price is some amount above the moving average. For the third algorithm, I want to try and gain experience using machine learning. I want to use the tensor flow library to make a neural network to suggest trades to make. The neural network will be trained with the price data of certain stocks. The hope is that what it learns from its training will be transferable to other stocks and for the future as well. The only real way to test this would be to have the algorithm trade what it has learned and to wait and see how the trades do in the future (this is not very practical for testing). I will use appropriate data structures to try and keep the running time of the algorithms as low as possible.

## System or Software Architecture Diagram
*Include a block-based diagram illustrating the architecture of your software or system. This should include major components, such as user interface elements, back-end services, and data storage, and show how they interact. Tools like Lucidchart, Draw.io, or even hand-drawn diagrams photographed and uploaded are acceptable. The purpose of the diagram is to help us understand the architecture of your solution. Diagram asthetics do not matter and will not be graded.*

This will include getting data from yfinance. How each algorithm uses the data. The algorithms being backtested using the framework I will create.

## Development Methodology
*Describe the methodology you'll use to organize and progress your work.*

The first step in my project will be obtaining and processing price data of stocks. I plan to get this data from the yahoo finance package in python.
Next I will make the backtesting framework
Next I will make the linear regression algorithm
Next I will test variations of the linear regression algorithm
Next I will make the mean reversion algorithm
Next I will test variations of the mean reversion algorithm
Next I will make the machine learning algorithm
Next I will test variations of the machine learning algorithm
I will summerize the results and make graphs of different preformances of the algorithms

I will test all the algorithms functionality with the same backtesting framework that I will construct.

*First, describe your plan for developing your project. This might include how (or if) you plan to use*


- *GitHub projects board to track progress on tasks and milestones*
- *GitHub issues to keep track of issues or problems*
- *Separate Git branches and/or GitHub pull requests for development*
- *GitHub actions for automated testing or deployment pipelines*
- *GitHub wiki for documentation and notes*

*Please also describe how (if) you plan test and evaluate your project's functionality. Do you plan to test manually or automatically? Any specific testing frameworks or libraries you plan to use?*

## Potential Challenges and Roadblocks
*Identify any potential challenges or roadblocks you anticipate facing during the development of your project. For each challenge, propose strategies or solutions you might use to overcome them, which may include getting help from the TAs/instructor. This could include technical hurdles or learning new technologies.*

I think the hardest parts will be making an interface where I can back test algorithms and making the machine learning algorithm.
I do not knnow anything about machine learning yet so I will need to watch tutorials and read up on how to make a nueral network.

## Additional Resources
*Include any additional resources, tutorials, or documentation that will be helpful for this project.*

## Conclusion and Future Work
*Wrap up your project description with any final thoughts, expectations, or goals not covered in the sections above. Also briefly discuss potential future work, i.e., what could be done next to improve the project.*
