from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import partial
from pathlib import Path

from IPython.display import Image
from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig, subplots
from matplotlib_venn import venn3
from pandas import DataFrame
from pymupdf import IRect, Page, Rect
from pymupdf import open as open_pdf
from seaborn import color_palette, displot, set_theme

from utils.constants import FIGURES_PATH, LOGOS_PATH, PRESENTATION_RESEARCH_PATH

THEME_STYLE = "whitegrid"
THEME_CONTEXT = "talk"
set_theme(style=THEME_STYLE, context=THEME_CONTEXT)
(GENERATED_FIGURES_PATH := FIGURES_PATH / "generated").mkdir(
    parents=True, exist_ok=True
)


def get_page_from_file(source_file: Path, page_number: int) -> Page:
    doc = open_pdf(str(source_file))  # open a document
    page = doc[page_number - 1]
    return page


def get_page_irect(page: Page, dpi: int) -> Rect:
    return page.get_pixmap(dpi=dpi).irect


def get_page_xy_centers(page_irect: Rect) -> tuple[int, int]:
    x0, y0, x1, y1 = page_irect
    return int((x1 - x0) // 2), int((y1 - y0) // 2)


def save_figure_from_page(
    source_file: Path,
    target_path: Path,
    page_number: int,
    dpi: int,
    top_left: tuple[int, int],
    bot_right: tuple[int, int],
):
    irect = IRect(top_left, bot_right)
    page = get_page_from_file(source_file, page_number)
    pix = page.get_pixmap(dpi=dpi, clip=irect)  # create a Pixmap
    pix.save(target_path)  # save the image as png


@dataclass(frozen=True)
class FigSize:
    width: int
    height: int

    @property
    def asdict(self) -> dict[str, int]:
        return {"width": self.width, "height": self.height}

    @property
    def astuple(self) -> tuple[int, int]:
        return (self.width, self.height)


class FigSizes(Enum):
    LOGO = FigSize(300, 300)
    DEMOG = FigSize(500, 500)
    FULL = FigSize(800, 800)
    XL = FigSize(1000, 1000)


def get_edm_venn(
    center_size: int = 8,
    sides_size: int = 10,
    sets_size: int = 6,
    figsize: tuple[int, int] = (10, 10),
    dpi: int = 200,
) -> tuple[Figure, Axis]:
    """Create a Venn diagram explaining EDM/LA."""
    fig, ax = subplots(figsize=figsize, dpi=dpi)
    subset_labels = [
        "Computer\nScience",  # CS
        "Education",  # Ed
        "Computer-Based\nLearning",
        "Statistics",  # Stats
        "Data Mining\nMachine Learning",
        "Educational\nStatistics",
        "Educational Data Mining\nLearning Analytics",
    ]
    subsets = [
        sets_size,  # CS
        sets_size,  # Ed
        sides_size,  # CBL
        sets_size,  # Stats
        sides_size,  # DM/ML
        sides_size,  # EdStats
        center_size,  # EDM/LA
    ]
    venn = venn3(subsets=subsets, set_labels=None, ax=ax)
    for name, label in zip(subset_labels, venn.subset_labels, strict=True):
        label.set_text(name)
    print("Educational Data Mining and Learning Analytics")
    print("Relationship with other fields of research")
    return fig, ax


def get_imd_band_displot(df: DataFrame) -> tuple[Figure, Axis]:
    """Create a distribution plot of IMD bands."""
    color_palette("Spectral", n_colors=4)
    ax = displot(
        df.sort_values("module_code"),
        x="final_result",
        col="imd_band",
        row="is_female",
        col_order=[f"{k}-{k + 10}%" for k in range(0, 100, 10)],
        binwidth=1,
        height=3,
        facet_kws={"margin_titles": True},
        stat="probability",
        hue="final_result",
    )
    print("Final Result by IMD Band and is_female")
    return ax


@dataclass(frozen=True)
class ProjectFigure:
    name: str
    description: str
    source_url: str = None
    source_table: str = None
    source_file: Path = None
    current_file: str = None
    func: Callable = None
    figsize: FigSize = FigSizes.FULL.value

    @property
    def filename(self) -> str:
        return f"{self.name.lower().replace(" ", "_")}.png"

    @property
    def filepath(self) -> Path:
        return GENERATED_FIGURES_PATH / self.filename

    @property
    def image(self) -> Image:
        if self.filepath.exists():
            ret = Image(filename=self.filepath, **self.figsize.asdict)
        elif self.current_file is not None:
            ret = Image(filename=self.current_file, **self.figsize.asdict)
        elif self.func is not None:
            self.func()
            savefig(self.filepath)
            ret = Image(filename=self.filepath, **self.figsize.asdict)
        else:
            raise ValueError("No image available")
        print(self.name)
        print(self.description)
        return ret


@dataclass(frozen=True)
class PaperFigure(ProjectFigure):
    pass


@dataclass(frozen=True)
class PresentationFigure(ProjectFigure):
    pass


class SharedFigures(Enum):
    FIRST30_DAYS_ACTIVE_BY_FINAL_RESULT = ProjectFigure(
        "First 30 Days Active by Final Result",
        "The distribution of student active days in the first 30 days of each course",
        current_file="n_days_active.png",
        source_table="first30.all_features",
    )
    ABROCA_BY_DEMOG_BALANCE = ProjectFigure(
        "ABROCA by Demographic Characteristic Balance",
        "The results of fitted regression models using ABROCA, ROCAUC, and demographic balance",
        current_file=FIGURES_PATH / "abroca_by_gender_dis.png",
        figsize=FigSizes.FULL.value,
    )
    ABROCA_LOGREG_ETREE = ProjectFigure(
        "ABROCA LogReg ETree Curves",
        "The ABROCA statistic rendered for two models split by is_female and has_disability",
        current_file=FIGURES_PATH / "abroca_logreg_271_0_etree_358_0_.png",
        figsize=FigSizes.XL.value,
    )
    BAYESIAN_ROPE_WINDOWPANE = ProjectFigure(
        "Windowpane Plot of Bayesian Model Comparisons",
        "A windowpane plot of Bayesian model comparisons using the results of a Bayesian signed rank test using a ROPE of 0.002",
        current_file=FIGURES_PATH / "bayes_window_20_16_top_100.png",
        figsize=FigSizes.FULL.value,
    )
    FREQUENTIST_ROPE_WINDOWPANE = ProjectFigure(
        "Windowpane Plot of Frequentist Model Comparisons",
        "A windowpane plot of frequentist model comparisons using the results of the non-parametric Nemenyi test",
        current_file=FIGURES_PATH / "freq_window_20_16_top_100.png",
        figsize=FigSizes.FULL.value,
    )
    ROC_BY_FIT_TIME = ProjectFigure(
        "ROC by Fit Time",
        "The mean and standard deviation of fit time and ROC AUC by model type",
        current_file=FIGURES_PATH / "roc_fit_by_mtype.png",
        figsize=FigSizes.XL.value,
    )
    N_TOTAL_CLICKS_BY_TOP_5TH_CLICKS = ProjectFigure(
        "Top Activities Total Clicks",
        "The total number of clicks on activities ranked in the top 5th percentile of activities as measured by student clicks",
        current_file=FIGURES_PATH / "n_total_clicks_by_top_5th_clicks.png",
        figsize=FigSizes.FULL.value,
    )
    N_DAYS_ACTIVE_BY_FINAL_RESULT = ProjectFigure(
        "Days Active by Final Result",
        "The distribution of student active days in each course",
        current_file=FIGURES_PATH / "n_days_active.png",
        figsize=FigSizes.FULL.value,
    )
    FINAL_RESULT_BY_STUDENT_COUNT = ProjectFigure(
        "Final Result by Student Count",
        "The distribution of final results by student count",
        current_file=FIGURES_PATH / "final_result_by_student.png",
        figsize=FigSizes.FULL.value,
    )
    COURSE_DOMAIN_BY_STUDENT_COUNT = ProjectFigure(
        "Course Domain by Student Count",
        "The distribution of course domains by student count",
        current_file=FIGURES_PATH / "course_domain_by_student.png",
        figsize=FigSizes.FULL.value,
    )
    HIGHEST_EDUCATION_BY_STUDENT_COUNT = ProjectFigure(
        "Highest Education by Student Count",
        "The distribution of highest education by student count",
        current_file=FIGURES_PATH / "highest_education_by_student.png",
        figsize=FigSizes.FULL.value,
    )
    REGION_BY_STUDENT_COUNT = ProjectFigure(
        "Region by Student Count",
        "The distribution of regions by student count",
        current_file=FIGURES_PATH / "region_by_student.png",
        figsize=FigSizes.FULL.value,
    )
    IMD_BAND_BY_STUDENT_COUNT = ProjectFigure(
        "IMD Band by Student Count",
        "The distribution of IMD bands by student count",
        current_file=FIGURES_PATH / "imd_band_by_student.png",
        figsize=FigSizes.FULL.value,
    )
    OULAD_15_IMD_BAND = ProjectFigure(
        "OULAD 15 IMD Band",
        "The distribution of IMD bands for the OULAD dataset and the 2015 data for the CCC module",
        current_file=FIGURES_PATH / "oulad_15_imd.png",
        figsize=FigSizes.FULL.value,
    )
    BAYES_ROPE_PDF = ProjectFigure(
        "Bayes On One Model",
        "A probability density function resulting from a Bayesian Signed Rank Test",
        current_file=FIGURES_PATH / "rope_rforest_519_0__etree_358_0_.png",
    )
    BAYES_ROPE_POSTERIOR = ProjectFigure(
        "Bayes On Two Models",
        "A Bayesian posterior plot resulting from a Bayesian hierarchical correlated t-test",
        current_file=FIGURES_PATH / "rope_on_two_hxg_boost_531_0__hxg_boost_540_0_.png",
    )
    HXGBOOST_ABROCA_IS_FEMALE = ProjectFigure(
        "HXGBoost ABROCA Is Female Demo",
        "The ABROCA statistic rendered for a model split by is_female",
        current_file=FIGURES_PATH / "hxg_boost_abroca_is_female_demo.png",
    )
    HXBOOST_ROC_DEMO = ProjectFigure(
        "HXBoost ROC Demo",
        "The ROC curve for an HXGBoost model",
        current_file=FIGURES_PATH / "hxg_boost_roc_demo.png",
    )


class PaperFigures(Enum):
    OULAD_COURSE_BREAKDOWN = PaperFigure(
        "OULAD Course Breakdown",
        "A breakdown of the OULAD dataset by course modules and domains",
        current_file="oulad_students_courses.png",
    )
    OULAD_ERD = PaperFigure(
        "OULAD ERD",
        "An Entity Relationship Diagram of the OULAD dataset",
        current_file="raw_model.png",
    )
    OULAD_VS_2015 = PaperFigure(
        "OULAD vs 2015",
        "An evaluation of the similarity between the published OULAD dataset and the 2015 data for CCC module",
        current_file="oulad_vs_15.png",
    )
    OULAD_VS_2015_AGES = PaperFigure(
        "OULAD vs 2015 Ages",
        "The distribution of student ages for OULAD data (blue) and 2015 data (red) for CCC module",
        current_file="oulad_15_age.png",
    )
    STUDENT_AGE_BANDS = PaperFigure(
        "Student Age Bands",
        "The distribution of student ages in the OULAD dataset",
        current_file="age_band_by_student.png",
    )
    STUDENT_FINAL_RESULTS = PaperFigure(
        "Student Final Results",
        "The distribution of final results in the OULAD dataset",
        current_file="final_result_by_student.png",
    )
    STUDENT_REGIONS = PaperFigure(
        "Student Regions",
        "The distribution of student regions in the OULAD dataset",
        current_file="region_by_student.png",
    )
    TOP_ACTIVITIES_TOTAL_CLICKS = PaperFigure(
        "Top Activities Total Clicks",
        "The total number of clicks on activities ranked in the top 5th percentile of activities as measured by student clicks",
        current_file="n_total_clicks_by_top_5th_clicks.png",
    )
    MODEL_TYPE_ROC_FIT = PaperFigure(
        "Model Type ROC Fit",
        "The mean and standard deviation of fit time and ROC AUC by model type",
        current_file="roc_fit_by_mtype.png",
    )
    ABROCA_REGRESSION = PaperFigure(
        "ABROCA Regression",
        "The relationship between ABROCA and demographic balance and mean test ROC AUC for the top four models",
        current_file="abroca_by_gender_dis.png",
    )


class PresentationFigures(Enum):
    FINAL_RESULT_BY_IMD_BAND = PresentationFigure(
        "Final Result by IMD Band",
        "The distribution of final results by Index of Multiple Deprivation band",
        source_table="landing.student_info",
    )
    MIN_DAYS_BEFORE_DUE_HIST = PresentationFigure(
        "Minimum Days Before Due Date Submitted Histogram",
        "The distribution of the minimum days before due date for each student",
        source_table="first30.all_features",
    )
    EDM_LA_VENN = PresentationFigure(
        "EDM LA Venn",
        "A Venn diagram showing the relationship between fields of research, Educational Data Mining, and Learning Analytics",
        func=get_edm_venn,
    )
    AUTOML_FEATURE_ENGINEERING = PresentationFigure(
        "AutoML Feature Engineering",
        "A comparison of the interpretability of features engineered using AutoML",
        source_file=PRESENTATION_RESEARCH_PATH
        / "AutoML Feature Engineering for Student Modeling Yields High Accuracy, but Limited Interpretability.pdf",
        current_file=FIGURES_PATH / "auto_fe.png",
        func=partial(
            save_figure_from_page,
            source_file=PRESENTATION_RESEARCH_PATH
            / "AutoML Feature Engineering for Student Modeling Yields High Accuracy, but Limited Interpretability.pdf",
            target_path=GENERATED_FIGURES_PATH / "AutoML_Feature_Engineering.png",
            page_number=18,
            dpi=300,
            top_left=(0, 0),
            bot_right=(500, 500),
        ),
    )
    CRITICAL_DIFFERENCE_NEMENYI = PresentationFigure(
        "Critical Difference Nemenyi",
        "Critical difference diagram based on results from post-hoc Nemenyi tests",
        source_file=PRESENTATION_RESEARCH_PATH
        / "Evaluating Predictive Models of Student Success Closing the Methodological Gap.pdf",
        current_file=FIGURES_PATH / "nemenyi_critical_dif.png",
        figsize=FigSizes.FULL.value,
        func=partial(
            save_figure_from_page,
            source_file=PRESENTATION_RESEARCH_PATH
            / "Evaluating Predictive Models of Student Success Closing the Methodological Gap.pdf",
            target_path=GENERATED_FIGURES_PATH / "Critical_Difference_Nemenyi.png",
            page_number=13,
            dpi=300,
            top_left=(25, 60),
            bot_right=(950, 410),
        ),
    )
    SCIKIT_LEARN_LOGO = PresentationFigure(
        "Scikit Learn",
        "Machine Learning Models & Components",
        current_file=LOGOS_PATH / "scikit-learn.png",
        figsize=FigSizes.LOGO.value,
    )
    SCIPY_LOGO = PresentationFigure(
        "SciPy",
        "Random Variables & Statistical Tests",
        current_file=LOGOS_PATH / "scipy.png",
        figsize=FigSizes.LOGO.value,
    )
    NUMPY_LOGO = PresentationFigure(
        "NumPy",
        "Array Computation",
        current_file=LOGOS_PATH / "numpy.png",
        figsize=FigSizes.LOGO.value,
    )
    SEABORN_LOGO = PresentationFigure(
        "Seaborn",
        "Visualizations",
        current_file=LOGOS_PATH / "seaborn.png",
        figsize=FigSizes.LOGO.value,
    )
    MATPLOTLIB_LOGO = PresentationFigure(
        "Matplotlib",
        "Visualizations",
        current_file=LOGOS_PATH / "matplotlib.png",
        figsize=FigSizes.LOGO.value,
    )
    PANDAS_LOGO = PresentationFigure(
        "Pandas",
        "Database Communication & Data Manipulation",
        current_file=LOGOS_PATH / "pandas.png",
        figsize=FigSizes.LOGO.value,
    )
    PSYCOPG2_LOGO = PresentationFigure(
        "Psycopg2",
        "Database Communication",
        current_file=LOGOS_PATH / "psycopg2.png",
        figsize=FigSizes.LOGO.value,
    )
    POSTGRESQL_LOGO = PresentationFigure(
        "PostgreSQL",
        "Database System",
        current_file=LOGOS_PATH / "postgresql.png",
        figsize=FigSizes.LOGO.value,
    )
    JUPYTER_LOGO = PresentationFigure(
        "Jupyter",
        "Notebook Engine",
        current_file=LOGOS_PATH / "jupyter.png",
        figsize=FigSizes.LOGO.value,
    )
    PYTHON_LOGO = PresentationFigure(
        "Python",
        "Programming Language",
        current_file=LOGOS_PATH / "python.png",
        figsize=FigSizes.LOGO.value,
    )
    IMD_BAND_IRELAND = PresentationFigure(
        "IMD Band Northern Ireland",
        "The distribution of IMD bands in Northern Ireland for 2017",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "imd.png",
        figsize=FigSizes.DEMOG.value,
    )
    AGE_BAND_BY_STUDENT = PresentationFigure(
        "Age Band by Student",
        "The distribution of age bands by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "age_band_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    IMD_BAND_BY_STUDENT = PresentationFigure(
        "IMD Band by Student",
        "The distribution of IMD bands by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "imd_band_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    REGION_BY_STUDENT = PresentationFigure(
        "Region by Student",
        "The distribution of regions by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "region_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    HIGHEST_EDUCATION_BY_STUDENT = PresentationFigure(
        "Highest Education by Student",
        "The distribution of highest education by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "highest_education_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    COURSE_DOMAIN_BY_STUDENT = PresentationFigure(
        "Course Domain by Student",
        "The distribution of course domains by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "course_domain_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    FINAL_RESULT_BY_STUDENT = PresentationFigure(
        "Final Result by Student",
        "The distribution of final results by student count",
        source_table="landing.student_info",
        current_file=FIGURES_PATH / "final_result_by_student.png",
        figsize=FigSizes.DEMOG.value,
    )
    OULAD_15_AGE = PresentationFigure(
        "OULAD 15 Age",
        "OULAD (Red & 2013-2014), vs 2015 data (Blue) - Age Distribution",
        current_file=FIGURES_PATH / "oulad_15_age.png",
        figsize=FigSizes.DEMOG.value,
    )
    OULAD_15_IMD = PresentationFigure(
        "OULAD 15 IMD",
        "OULAD (Red & 2013-2014), vs 2015 data (Blue) - IMD Distribution",
        current_file=FIGURES_PATH / "oulad_15_imd.png",
        figsize=FigSizes.DEMOG.value,
    )
    OULAD_VS_15 = PresentationFigure(
        "OULAD vs 15",
        "An evaluation of the similarity between the published OULAD dataset and the 2015 data for CCC module",
        current_file=FIGURES_PATH / "oulad_vs_15.png",
    )
    OULAD_STUDENT_COURSES = PresentationFigure(
        "OULADs Students Courses",
        "A breakdown of the OULAD dataset by course modules and domains",
        current_file=FIGURES_PATH / "oulad_students_courses.png",
    )
    SOURCE_ERD_MODEL = PresentationFigure(
        "Source ERD Model",
        "An Entity Relationship Diagram of the OULAD dataset",
        current_file=FIGURES_PATH / "raw_model.png",
        figsize=FigSizes.FULL.value,
    )
    TABLES_BY_SCHEMA = PresentationFigure(
        "Tables by Schema",
        "The number of tables in each schema",
        source_table="landing.table_counts",
        current_file=FIGURES_PATH / "tables_by_schema.png",
        figsize=FigSizes.FULL.value,
    )
