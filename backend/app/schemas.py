from pydantic import BaseModel


class EmployeeInput(BaseModel):
    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int


class PredictionResponse(BaseModel):
    attrition_probability: float
    prediction: str
    risk_level: str
    threshold: float
    risk_factors: list[str]


class FeatureImportanceItem(BaseModel):
    feature: str
    importance_mean: float
    importance_std: float
    cv: float


class TestMetrics(BaseModel):
    roc_auc: float
    accuracy: float
    precision_yes: float
    recall_yes: float
    f1_yes: float


class ConfusionMatrix(BaseModel):
    tn: int
    fp: int
    fn: int
    tp: int


class ClassDistribution(BaseModel):
    no: int
    yes: int


class ModelMetricsResponse(BaseModel):
    model_name: str
    validation_method: str
    threshold_strategy: str
    threshold: float
    test_metrics: TestMetrics
    confusion_matrix: ConfusionMatrix
    class_distribution: ClassDistribution
