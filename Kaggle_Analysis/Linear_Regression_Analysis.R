# Required Libraries
library(ggplot2)
library(ggsci)
library(RColorBrewer)
library(writexl)
library(ggpubr)

# Read in Kaggle DF
kaggle_df <- read.csv(file = "Speed_Dating_Data - Date_Analysis.csv", header = TRUE, sep = ",")

# Factorize individual's variables
kaggle_df$gender <- factor(kaggle_df$gender)
kaggle_df$career_c <- factor(kaggle_df$career_c)
kaggle_df$field_cd <- factor(kaggle_df$field_cd)
kaggle_df$race <- factor(kaggle_df$race)
kaggle_df$dec <- factor(kaggle_df$dec)
kaggle_df$samerace <- factor(kaggle_df$samerace)

# Factorize partner's variables
kaggle_df$race_o <- factor(kaggle_df$race_o)
kaggle_df$dec_o <- factor(kaggle_df$dec_o)

# Create variable for partner's field_cd, career_c, same_field, same_career
partner_rows <- c()
for (index in 1:nrow(kaggle_df)) {
  partner_iid <- kaggle_df$pid[index]
  partner_row <- match(partner_iid, kaggle_df$iid)
  partner_rows <- c(partner_rows, partner_row)
}

kaggle_df$field_cd_o <- kaggle_df[partner_rows, ]$field_cd
kaggle_df$career_c_o <- kaggle_df[partner_rows, ]$career_c

kaggle_df$same_field <- rep(0, nrow(kaggle_df))
kaggle_df$same_career <- rep(0, nrow(kaggle_df))

for (index in 1:nrow(kaggle_df)) {
  if (!is.na(kaggle_df$field_cd[index]) & !is.na(kaggle_df$field_cd_o[index])) {
    if (kaggle_df$field_cd[index] == kaggle_df$field_cd_o[index]) {
      kaggle_df$same_field[index] <- 1
    } 
  }
  
  if (!is.na(kaggle_df$career_c[index]) & !is.na(kaggle_df$career_c_o[index]))  {
    if (kaggle_df$career_c[index] == kaggle_df$career_c_o[index]) {
      kaggle_df$same_career[index] <- 1
    }
  }
}
kaggle_df$same_field <- factor(kaggle_df$same_field,
                               levels=c(0, 1),
                               labels=c("Different Major", "Same Major"))
kaggle_df$same_career <- factor(kaggle_df$same_career,
                               levels=c(0, 1),
                               labels=c("Different Career", "Same Career"))
kaggle_df$samerace <- factor(kaggle_df$samerace,
                             levels=c(0, 1),
                             labels=c("Different Race", "Same Race"))
kaggle_df$same_career <- factor(kaggle_df$same_career)

write_xlsx(kaggle_df, "Kaggle_Data - Individual_Dates_Clean.xlsx")

# Linear Regression Code
summary(lm(like ~ same_field + samerace + gender + field_cd + field_cd_o + race + race_o, data = kaggle_df))
summary(lm(like ~ same_career + samerace + gender + career_c + career_c_o + race + race_o, data = kaggle_df))

# Logistic Regression Code
log_r <- glm(dec ~ same_field + samerace + gender + field_cd + field_cd_o + race + race_o, data = kaggle_df, binomial)
log_r <- glm(dec ~ same_career + samerace + gender + career_c + career_c_o + race + race_o, data = kaggle_df, binomial)
summary(log_r)
exp(coef(log_r))

# Figure generation and hypothesis testing
cmpr_kaggle <- list(c("Same Career", "Different Career"))
ggplot(data = kaggle_df, aes(x = same_career, y = like, fill = same_career)) + 
  geom_violin(adjust = 1.2, trim = FALSE, width = 0.5) + 
  geom_boxplot(width = 0.2, color = "black", fill = "white") + 
  ylim(0, 13) + xlab("") + ylab("Likeability Score") + scale_fill_discrete(name = "") +
  stat_compare_means(comparisons = cmpr_kaggle, tip.length=0.01,
                     method = "t.test", label = "p.signif", label.y = c(12),
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1), symbols = c("****", "***", "**", "*", "ns"))) +
  scale_color_npg() + theme_bw()
dev.print(png, filename="Box and Violin Plot - Likeability (Same Career).png", units="in", height=5, width=5, res=300)

t.test(kaggle_df[kaggle_df$same_career == "Different Career", ]$like, kaggle_df[kaggle_df$same_career == "Same Career", ]$like)

cmpr_race <- list(c("Same Race", "Different Race"))
ggplot(data = kaggle_df,  aes(x =  samerace, y = int_corr, fill = samerace)) +
  geom_violin(adjust = 1.2, trim = FALSE, width = 0.5) + 
  geom_boxplot(width = 0.2, color = "black", fill = "white") +
  ylim(-1, 1.3) + xlab("") + ylab("Shared Interest Correlation") + scale_fill_discrete(name = "") +
  stat_compare_means(comparisons = cmpr_race, tip.length=0.01,
                     method = "t.test", label = "p.signif", label.y = c(1.2),
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1), symbols = c("****", "***", "**", "*", "ns"))) +
  scale_color_npg() + theme_bw()
dev.print(png, filename="Box and Violin Plot - Shared Interest.png", units="in", height=5, width=5, res=300)

# Miscellaneous code for testing things
temp <- kaggle_df[kaggle_df$dec == 1, ]
ggplot(data = temp, aes(x = same_field)) + geom_bar(aes(y = ..count..))

ggplot(kaggle_df, aes(x = same_field, y = dec))

diff_field_df <- kaggle_df[kaggle_df$same_field == 0, ]
same_field_df <- kaggle_df[kaggle_df$same_field == 1, ]
said_yes_df <- data.frame(same_field = c("Different Major", "Same Major"),
                          yes_proportion = c(nrow(kaggle_df[kaggle_df$same_field == "Different Major" & kaggle_df$dec == 1, ]) / 
                                               nrow(kaggle_df[kaggle_df$same_field == "Different Major", ]),
                                             nrow(kaggle_df[kaggle_df$same_field == "Same Major" & kaggle_df$dec == 1, ]) / 
                                               nrow(kaggle_df[kaggle_df$same_field == "Same Major", ])))

said_yes_career_df <- data.frame(same_field = c("Different Career", "Same Career"),
                          yes_proportion = c(nrow(kaggle_df[kaggle_df$same_career == "Different Career" & kaggle_df$dec == 1, ]) / 
                                               nrow(kaggle_df[kaggle_df$same_career == "Different Career", ]),
                                             nrow(kaggle_df[kaggle_df$same_career == "Same Career" & kaggle_df$dec == 1, ]) / 
                                               nrow(kaggle_df[kaggle_df$same_career == "Same Career", ])))

proportions_df <- data.frame(same = c("Same Major", "Same Career", "Same Major", "Same Career"),
                             data = c("Kaggle", "Kaggle", "Census", "Census"),
                             proportions = c(0.132, 0.190, 0.254, 0.343))

ggplot(proportions_df, aes(x = data, y = proportions, fill = same)) + geom_bar(position = "dodge", stat="identity", width=0.5) +
  xlab("") + ylab("Proportion of Individuals Married/Attracted") + scale_fill_discrete("") +
  scale_color_npg() + theme_bw()
dev.print(png, filename="Bar Plot - Proportion Kaggle vs. Census.png", units="in", height=5, width=5, res=300)

nrow(kaggle_df[kaggle_df$same_field == "Different Major" & kaggle_df$dec == 1, ]) / 
  nrow(kaggle_df[kaggle_df$dec == 1, ])

nrow(kaggle_df[kaggle_df$same_field == "Same Major" & kaggle_df$dec == 1, ]) / 
  nrow(kaggle_df[kaggle_df$dec == 1, ])

nrow(kaggle_df[kaggle_df$same_career == 1 & kaggle_df$dec == 1, ]) / 
  nrow(kaggle_df[kaggle_df$dec == 1, ])

# Proportions test
prop.test(x = c(2849, 669), n = c(6858, 1520))
prop.test(x = c(466, 669), n = c(3518, 3518))
prop.test(x = c(3306, 4456), n = c(12992, 12928))
prop.test(x = c(466, 3306), n = c(3518, 12992))
prop.test(x = c(3052, 466), n = c(7416, 962))
prop.test(669, 3518)
prop.test(466, 3518)

wilcox.test(attr~same_field, data=kaggle_df)
t.test(diff_field_df$attr, same_field_df$attr)
t.test(diff_field_df$like, same_field_df$like)

ggplot(said_yes_career_df, aes(same_field, yes_proportion, fill=same_field)) + geom_col(width=0.5) +
  xlab("") + ylab("Proportion of 'Yes to Second-Date'") + scale_fill_discrete(name = "") +
  scale_color_npg() + theme_bw()
dev.print(png, filename="Bar Plot - Proportion of Second Date (Career).png", units="in", height=5, width=5, res=300)


