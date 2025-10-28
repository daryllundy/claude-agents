"""
Data Science Agent - Specialized agent for data science and ML tasks
"""

from anthropic import Anthropic
import os

class DataScienceAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a data science specialist with expertise in:

1. Data Preprocessing:
   - Data cleaning and validation
   - Missing value handling
   - Outlier detection and treatment
   - Feature scaling (standardization, normalization)
   - Encoding categorical variables
   - Data transformation
   - Train/test/validation splits

2. Feature Engineering:
   - Feature selection techniques
   - Feature extraction
   - Dimensionality reduction (PCA, t-SNE)
   - Polynomial features
   - Interaction terms
   - Domain-specific features
   - Time-based features

3. Machine Learning:
   - Supervised learning (classification, regression)
   - Unsupervised learning (clustering, anomaly detection)
   - Model selection
   - Hyperparameter tuning
   - Cross-validation
   - Ensemble methods
   - Deep learning basics

4. Model Evaluation:
   - Classification metrics (accuracy, precision, recall, F1, ROC-AUC)
   - Regression metrics (MSE, RMSE, MAE, R²)
   - Confusion matrices
   - Learning curves
   - Bias-variance tradeoff
   - Model interpretation (SHAP, LIME)

5. Libraries & Frameworks:
   - NumPy, Pandas, Polars
   - Scikit-learn
   - TensorFlow, PyTorch, Keras
   - XGBoost, LightGBM, CatBoost
   - Statsmodels
   - Matplotlib, Seaborn, Plotly

6. MLOps:
   - Experiment tracking (MLflow, Weights & Biases)
   - Model versioning
   - Pipeline orchestration
   - Model deployment
   - Monitoring and drift detection
   - A/B testing

7. Data Visualization:
   - Exploratory data analysis
   - Distribution plots
   - Correlation analysis
   - Feature importance visualization
   - Model performance visualization
   - Interactive dashboards

8. Statistical Analysis:
   - Hypothesis testing
   - Confidence intervals
   - A/B testing
   - Time series analysis
   - Bayesian methods
   - Causal inference

Best practices:
- Start with exploratory data analysis
- Establish baseline models first
- Use cross-validation properly
- Check for data leakage
- Document experiments thoroughly
- Version control data and models
- Monitor for model drift
- Consider computational efficiency
- Validate assumptions
- Ensure reproducibility"""

    def execute(self, task: str, context: dict = None) -> dict:
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=6000,
            system=self.system_prompt,
            messages=messages
        )
        
        return self._parse_response(response)
    
    def _build_prompt(self, task: str, context: dict = None) -> str:
        prompt = f"Task: {task}\n\n"
        
        if context:
            prompt += "Context:\n"
            if context.get("data_description"):
                prompt += f"- Data: {context['data_description']}\n"
            if context.get("problem_type"):
                prompt += f"- Problem Type: {context['problem_type']}\n"
            if context.get("target"):
                prompt += f"- Target Variable: {context['target']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        pipelines = []
        
        for language, code in code_blocks:
            pipelines.append({"language": language, "content": code.strip()})
        
        return {"response": text_content, "pipelines": pipelines}


if __name__ == "__main__":
    agent = DataScienceAgent()
    result = agent.execute("Create a preprocessing pipeline for customer churn prediction", 
                          {"problem_type": "binary classification", "target": "churned"})
