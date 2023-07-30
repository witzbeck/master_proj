select
 m.student_id

,sum(is_dataplus*m.n                    )        dataplus_n            
,sum(is_dataplus*m.avg_date             )        dataplus_avg_date     
,sum(is_dataplus*m.var_date             )        dataplus_var_date     
,sum(is_dataplus*m.stddev_date          )        dataplus_stddev_date  
,sum(is_dataplus*m.skew_date            )        dataplus_skew_date    
,sum(is_dataplus*m.kurt_date            )        dataplus_kurt_date    
,sum(is_dataplus*m.avg_clicks           )        dataplus_avg_clicks   
,sum(is_dataplus*m.var_clicks           )        dataplus_var_clicks   
,sum(is_dataplus*m.stddev_clicks        )        dataplus_stddev_clicks
,sum(is_dataplus*m.skew_clicks          )        dataplus_skew_clicks  
,sum(is_dataplus*m.kurt_clicks          )        dataplus_kurt_clicks  
,sum(is_dataplus*m.fp_coeff             )        dataplus_fp_coeff     
,sum(is_dualpane*m.n                    )        dualpane_n            
,sum(is_dualpane*m.avg_date             )        dualpane_avg_date     
,sum(is_dualpane*m.var_date             )        dualpane_var_date     
,sum(is_dualpane*m.stddev_date          )        dualpane_stddev_date  
,sum(is_dualpane*m.skew_date            )        dualpane_skew_date    
,sum(is_dualpane*m.kurt_date            )        dualpane_kurt_date    
,sum(is_dualpane*m.avg_clicks           )        dualpane_avg_clicks   
,sum(is_dualpane*m.var_clicks           )        dualpane_var_clicks   
,sum(is_dualpane*m.stddev_clicks        )        dualpane_stddev_clicks
,sum(is_dualpane*m.skew_clicks          )        dualpane_skew_clicks  
,sum(is_dualpane*m.kurt_clicks          )        dualpane_kurt_clicks  
,sum(is_dualpane*m.fp_coeff             )        dualpane_fp_coeff     
,sum(is_folder*m.n                      )        folder_n            
,sum(is_folder*m.avg_date               )        folder_avg_date     
,sum(is_folder*m.var_date               )        folder_var_date     
,sum(is_folder*m.stddev_date            )        folder_stddev_date  
,sum(is_folder*m.skew_date              )        folder_skew_date    
,sum(is_folder*m.kurt_date              )        folder_kurt_date    
,sum(is_folder*m.avg_clicks             )        folder_avg_clicks   
,sum(is_folder*m.var_clicks             )        folder_var_clicks   
,sum(is_folder*m.stddev_clicks          )        folder_stddev_clicks
,sum(is_folder*m.skew_clicks            )        folder_skew_clicks  
,sum(is_folder*m.kurt_clicks            )        folder_kurt_clicks  
,sum(is_folder*m.fp_coeff               )        folder_fp_coeff     
,sum(is_forumng*m.n                     )        forumng_n            
,sum(is_forumng*m.avg_date              )        forumng_avg_date     
,sum(is_forumng*m.var_date              )        forumng_var_date     
,sum(is_forumng*m.stddev_date           )        forumng_stddev_date  
,sum(is_forumng*m.skew_date             )        forumng_skew_date    
,sum(is_forumng*m.kurt_date             )        forumng_kurt_date    
,sum(is_forumng*m.avg_clicks            )        forumng_avg_clicks   
,sum(is_forumng*m.var_clicks            )        forumng_var_clicks   
,sum(is_forumng*m.stddev_clicks         )        forumng_stddev_clicks
,sum(is_forumng*m.skew_clicks           )        forumng_skew_clicks  
,sum(is_forumng*m.kurt_clicks           )        forumng_kurt_clicks  
,sum(is_forumng*m.fp_coeff              )        forumng_fp_coeff     
,sum(is_glossary*m.n                    )        glossary_n            
,sum(is_glossary*m.avg_date             )        glossary_avg_date     
,sum(is_glossary*m.var_date             )        glossary_var_date     
,sum(is_glossary*m.stddev_date          )        glossary_stddev_date  
,sum(is_glossary*m.skew_date            )        glossary_skew_date    
,sum(is_glossary*m.kurt_date            )        glossary_kurt_date    
,sum(is_glossary*m.avg_clicks           )        glossary_avg_clicks   
,sum(is_glossary*m.var_clicks           )        glossary_var_clicks   
,sum(is_glossary*m.stddev_clicks        )        glossary_stddev_clicks
,sum(is_glossary*m.skew_clicks          )        glossary_skew_clicks  
,sum(is_glossary*m.kurt_clicks          )        glossary_kurt_clicks  
,sum(is_glossary*m.fp_coeff             )        glossary_fp_coeff     
,sum(is_homepage*m.n                    )        homepage_n            
,sum(is_homepage*m.avg_date             )        homepage_avg_date     
,sum(is_homepage*m.var_date             )        homepage_var_date     
,sum(is_homepage*m.stddev_date          )        homepage_stddev_date  
,sum(is_homepage*m.skew_date            )        homepage_skew_date    
,sum(is_homepage*m.kurt_date            )        homepage_kurt_date    
,sum(is_homepage*m.avg_clicks           )        homepage_avg_clicks   
,sum(is_homepage*m.var_clicks           )        homepage_var_clicks   
,sum(is_homepage*m.stddev_clicks        )        homepage_stddev_clicks
,sum(is_homepage*m.skew_clicks          )        homepage_skew_clicks  
,sum(is_homepage*m.kurt_clicks          )        homepage_kurt_clicks  
,sum(is_homepage*m.fp_coeff             )        homepage_fp_coeff     
,sum(is_htmlactivity*m.n                )        html_activity_n            
,sum(is_htmlactivity*m.avg_date         )        html_activity_avg_date     
,sum(is_htmlactivity*m.var_date         )        html_activity_var_date     
,sum(is_htmlactivity*m.stddev_date      )        html_activity_stddev_date  
,sum(is_htmlactivity*m.skew_date        )        html_activity_skew_date    
,sum(is_htmlactivity*m.kurt_date        )        html_activity_kurt_date    
,sum(is_htmlactivity*m.avg_clicks       )        html_activity_avg_clicks   
,sum(is_htmlactivity*m.var_clicks       )        html_activity_var_clicks   
,sum(is_htmlactivity*m.stddev_clicks    )        html_activity_stddev_clicks
,sum(is_htmlactivity*m.skew_clicks      )        html_activity_skew_clicks  
,sum(is_htmlactivity*m.kurt_clicks      )        html_activity_kurt_clicks  
,sum(is_htmlactivity*m.fp_coeff         )        html_activity_fp_coeff     
,sum(is_oucollaborate*m.n               )        oucollaborate_n            
,sum(is_oucollaborate*m.avg_date        )        oucollaborate_avg_date     
,sum(is_oucollaborate*m.var_date        )        oucollaborate_var_date     
,sum(is_oucollaborate*m.stddev_date     )        oucollaborate_stddev_date  
,sum(is_oucollaborate*m.skew_date       )        oucollaborate_skew_date    
,sum(is_oucollaborate*m.kurt_date       )        oucollaborate_kurt_date    
,sum(is_oucollaborate*m.avg_clicks      )        oucollaborate_avg_clicks   
,sum(is_oucollaborate*m.var_clicks      )        oucollaborate_var_clicks   
,sum(is_oucollaborate*m.stddev_clicks   )        oucollaborate_stddev_clicks
,sum(is_oucollaborate*m.skew_clicks     )        oucollaborate_skew_clicks  
,sum(is_oucollaborate*m.kurt_clicks     )        oucollaborate_kurt_clicks  
,sum(is_oucollaborate*m.fp_coeff        )        oucollaborate_fp_coeff     
,sum(is_oucontent*m.n                   )        oucontent_n            
,sum(is_oucontent*m.avg_date            )        oucontent_avg_date     
,sum(is_oucontent*m.var_date            )        oucontent_var_date     
,sum(is_oucontent*m.stddev_date         )        oucontent_stddev_date  
,sum(is_oucontent*m.skew_date           )        oucontent_skew_date    
,sum(is_oucontent*m.kurt_date           )        oucontent_kurt_date    
,sum(is_oucontent*m.avg_clicks          )        oucontent_avg_clicks   
,sum(is_oucontent*m.var_clicks          )        oucontent_var_clicks   
,sum(is_oucontent*m.stddev_clicks       )        oucontent_stddev_clicks
,sum(is_oucontent*m.skew_clicks         )        oucontent_skew_clicks  
,sum(is_oucontent*m.kurt_clicks         )        oucontent_kurt_clicks  
,sum(is_oucontent*m.fp_coeff            )        oucontent_fp_coeff     
,sum(is_ouelluminate*m.n                )        ouelluminate_n            
,sum(is_ouelluminate*m.avg_date         )        ouelluminate_avg_date     
,sum(is_ouelluminate*m.var_date         )        ouelluminate_var_date     
,sum(is_ouelluminate*m.stddev_date      )        ouelluminate_stddev_date  
,sum(is_ouelluminate*m.skew_date        )        ouelluminate_skew_date    
,sum(is_ouelluminate*m.kurt_date        )        ouelluminate_kurt_date    
,sum(is_ouelluminate*m.avg_clicks       )        ouelluminate_avg_clicks   
,sum(is_ouelluminate*m.var_clicks       )        ouelluminate_var_clicks   
,sum(is_ouelluminate*m.stddev_clicks    )        ouelluminate_stddev_clicks
,sum(is_ouelluminate*m.skew_clicks      )        ouelluminate_skew_clicks  
,sum(is_ouelluminate*m.kurt_clicks      )        ouelluminate_kurt_clicks  
,sum(is_ouelluminate*m.fp_coeff         )        ouelluminate_fp_coeff     
,sum(is_ouwiki*m.n                      )        ouwiki_n            
,sum(is_ouwiki*m.avg_date               )        ouwiki_avg_date     
,sum(is_ouwiki*m.var_date               )        ouwiki_var_date     
,sum(is_ouwiki*m.stddev_date            )        ouwiki_stddev_date  
,sum(is_ouwiki*m.skew_date              )        ouwiki_skew_date    
,sum(is_ouwiki*m.kurt_date              )        ouwiki_kurt_date    
,sum(is_ouwiki*m.avg_clicks             )        ouwiki_avg_clicks   
,sum(is_ouwiki*m.var_clicks             )        ouwiki_var_clicks   
,sum(is_ouwiki*m.stddev_clicks          )        ouwiki_stddev_clicks
,sum(is_ouwiki*m.skew_clicks            )        ouwiki_skew_clicks  
,sum(is_ouwiki*m.kurt_clicks            )        ouwiki_kurt_clicks  
,sum(is_ouwiki*m.fp_coeff               )        ouwiki_fp_coeff     
,sum(is_page*m.n                        )        page_n            
,sum(is_page*m.avg_date                 )        page_avg_date     
,sum(is_page*m.var_date                 )        page_var_date     
,sum(is_page*m.stddev_date              )        page_stddev_date  
,sum(is_page*m.skew_date                )        page_skew_date    
,sum(is_page*m.kurt_date                )        page_kurt_date    
,sum(is_page*m.avg_clicks               )        page_avg_clicks   
,sum(is_page*m.var_clicks               )        page_var_clicks   
,sum(is_page*m.stddev_clicks            )        page_stddev_clicks
,sum(is_page*m.skew_clicks              )        page_skew_clicks  
,sum(is_page*m.kurt_clicks              )        page_kurt_clicks  
,sum(is_page*m.fp_coeff                 )        page_fp_coeff     
,sum(is_questionnaire*m.n               )        questionnaire_n            
,sum(is_questionnaire*m.avg_date        )        questionnaire_avg_date     
,sum(is_questionnaire*m.var_date        )        questionnaire_var_date     
,sum(is_questionnaire*m.stddev_date     )        questionnaire_stddev_date  
,sum(is_questionnaire*m.skew_date       )        questionnaire_skew_date    
,sum(is_questionnaire*m.kurt_date       )        questionnaire_kurt_date    
,sum(is_questionnaire*m.avg_clicks      )        questionnaire_avg_clicks   
,sum(is_questionnaire*m.var_clicks      )        questionnaire_var_clicks   
,sum(is_questionnaire*m.stddev_clicks   )        questionnaire_stddev_clicks
,sum(is_questionnaire*m.skew_clicks     )        questionnaire_skew_clicks  
,sum(is_questionnaire*m.kurt_clicks     )        questionnaire_kurt_clicks  
,sum(is_questionnaire*m.fp_coeff        )        questionnaire_fp_coeff     
,sum(is_externalquiz*m.n                )        externalquiz_n            
,sum(is_externalquiz*m.avg_date         )        externalquiz_avg_date     
,sum(is_externalquiz*m.var_date         )        externalquiz_var_date     
,sum(is_externalquiz*m.stddev_date      )        externalquiz_stddev_date  
,sum(is_externalquiz*m.skew_date        )        externalquiz_skew_date    
,sum(is_externalquiz*m.kurt_date        )        externalquiz_kurt_date    
,sum(is_externalquiz*m.avg_clicks       )        externalquiz_avg_clicks   
,sum(is_externalquiz*m.var_clicks       )        externalquiz_var_clicks   
,sum(is_externalquiz*m.stddev_clicks    )        externalquiz_stddev_clicks
,sum(is_externalquiz*m.skew_clicks      )        externalquiz_skew_clicks  
,sum(is_externalquiz*m.kurt_clicks      )        externalquiz_kurt_clicks  
,sum(is_externalquiz*m.fp_coeff         )        externalquiz_fp_coeff     
,sum(is_quiz*m.n                        )        quiz_n            
,sum(is_quiz*m.avg_date                 )        quiz_avg_date     
,sum(is_quiz*m.var_date                 )        quiz_var_date     
,sum(is_quiz*m.stddev_date              )        quiz_stddev_date  
,sum(is_quiz*m.skew_date                )        quiz_skew_date    
,sum(is_quiz*m.kurt_date                )        quiz_kurt_date    
,sum(is_quiz*m.avg_clicks               )        quiz_avg_clicks   
,sum(is_quiz*m.var_clicks               )        quiz_var_clicks   
,sum(is_quiz*m.stddev_clicks            )        quiz_stddev_clicks
,sum(is_quiz*m.skew_clicks              )        quiz_skew_clicks  
,sum(is_quiz*m.kurt_clicks              )        quiz_kurt_clicks  
,sum(is_quiz*m.fp_coeff                 )        quiz_fp_coeff     
,sum(is_repeatactivity*m.n              )        repeatactivity_n            
,sum(is_repeatactivity*m.avg_date       )        repeatactivity_avg_date     
,sum(is_repeatactivity*m.var_date       )        repeatactivity_var_date     
,sum(is_repeatactivity*m.stddev_date    )        repeatactivity_stddev_date  
,sum(is_repeatactivity*m.skew_date      )        repeatactivity_skew_date    
,sum(is_repeatactivity*m.kurt_date      )        repeatactivity_kurt_date    
,sum(is_repeatactivity*m.avg_clicks     )        repeatactivity_avg_clicks   
,sum(is_repeatactivity*m.var_clicks     )        repeatactivity_var_clicks   
,sum(is_repeatactivity*m.stddev_clicks  )        repeatactivity_stddev_clicks
,sum(is_repeatactivity*m.skew_clicks    )        repeatactivity_skew_clicks  
,sum(is_repeatactivity*m.kurt_clicks    )        repeatactivity_kurt_clicks  
,sum(is_repeatactivity*m.fp_coeff       )        repeatactivity_fp_coeff     
,sum(is_resource*m.n                    )        resource_n            
,sum(is_resource*m.avg_date             )        resource_avg_date     
,sum(is_resource*m.var_date             )        resource_var_date     
,sum(is_resource*m.stddev_date          )        resource_stddev_date  
,sum(is_resource*m.skew_date            )        resource_skew_date    
,sum(is_resource*m.kurt_date            )        resource_kurt_date    
,sum(is_resource*m.avg_clicks           )        resource_avg_clicks   
,sum(is_resource*m.var_clicks           )        resource_var_clicks   
,sum(is_resource*m.stddev_clicks        )        resource_stddev_clicks
,sum(is_resource*m.skew_clicks          )        resource_skew_clicks  
,sum(is_resource*m.kurt_clicks          )        resource_kurt_clicks  
,sum(is_resource*m.fp_coeff             )        resource_fp_coeff     
,sum(is_sharedsubpage*m.n               )        sharedsubpage_n            
,sum(is_sharedsubpage*m.avg_date        )        sharedsubpage_avg_date     
,sum(is_sharedsubpage*m.var_date        )        sharedsubpage_var_date     
,sum(is_sharedsubpage*m.stddev_date     )        sharedsubpage_stddev_date  
,sum(is_sharedsubpage*m.skew_date       )        sharedsubpage_skew_date    
,sum(is_sharedsubpage*m.kurt_date       )        sharedsubpage_kurt_date    
,sum(is_sharedsubpage*m.avg_clicks      )        sharedsubpage_avg_clicks   
,sum(is_sharedsubpage*m.var_clicks      )        sharedsubpage_var_clicks   
,sum(is_sharedsubpage*m.stddev_clicks   )        sharedsubpage_stddev_clicks
,sum(is_sharedsubpage*m.skew_clicks     )        sharedsubpage_skew_clicks  
,sum(is_sharedsubpage*m.kurt_clicks     )        sharedsubpage_kurt_clicks  
,sum(is_sharedsubpage*m.fp_coeff        )        sharedsubpage_fp_coeff     
,sum(is_subpage*m.n                     )        subpage_n            
,sum(is_subpage*m.avg_date              )        subpage_avg_date     
,sum(is_subpage*m.var_date              )        subpage_var_date     
,sum(is_subpage*m.stddev_date           )        subpage_stddev_date  
,sum(is_subpage*m.skew_date             )        subpage_skew_date    
,sum(is_subpage*m.kurt_date             )        subpage_kurt_date    
,sum(is_subpage*m.avg_clicks            )        subpage_avg_clicks   
,sum(is_subpage*m.var_clicks            )        subpage_var_clicks   
,sum(is_subpage*m.stddev_clicks         )        subpage_stddev_clicks
,sum(is_subpage*m.skew_clicks           )        subpage_skew_clicks  
,sum(is_subpage*m.kurt_clicks           )        subpage_kurt_clicks  
,sum(is_subpage*m.fp_coeff              )        subpage_fp_coeff     
,sum(is_url*m.n                         )        url_n             
,sum(is_url*m.avg_date                  )        url_avg_date     
,sum(is_url*m.var_date                  )        url_var_date     
,sum(is_url*m.stddev_date               )        url_stddev_date  
,sum(is_url*m.skew_date                 )        url_skew_date    
,sum(is_url*m.kurt_date                 )        url_kurt_date    
,sum(is_url*m.avg_clicks                )        url_avg_clicks   
,sum(is_url*m.var_clicks                )        url_var_clicks   
,sum(is_url*m.stddev_clicks             )        url_stddev_clicks
,sum(is_url*m.skew_clicks               )        url_skew_clicks  
,sum(is_url*m.kurt_clicks               )        url_kurt_clicks  
,sum(is_url*m.fp_coeff                  )        url_fp_coeff     
into first30.mom_interactions_per_type_1234_pivot
from first30.mom_interactions_per_type_1234 m
join main.v_activity_types_onehot v on v.id=m.activity_type_id
group by student_id