# analyze steem data scraped from web
# author: matt hoover <matthew.a.hoover at gmail.com>
library(ggnet)
library(ggplot2)
library(statnet)

# load data
el <- read.csv('steem_edgelist.csv', header = TRUE, sep = ',',
               stringsAsFactors = FALSE)
attrs <- read.csv('steem_user_attributes.csv', header = TRUE, sep = ',',
                  stringsAsFactors = FALSE)

# clean up attributes
attrs$reward_vesting_bal <- as.numeric(gsub(' VESTS', '', attrs$reward_vesting_bal))
attrs$reward_vesting_steem <- as.numeric(gsub(' STEEM', '', attrs$reward_vesting_steem))
attrs$days_since_last_post <- as.numeric(strptime('2017-05-13 14:00:00',
                                        format='%Y-%m-%d %H:%M:%S') -
                               strptime(attrs$last_post,
                                        format='%Y-%m-%dT%H:%M:%S'), units = 'days')

# create network
net <- network(el)

# gather/add attributes to network object
attrs <- merge(attrs, data.frame(name = net %v% 'vertex.names'), by = 'name',
               all = TRUE)
VARS_TO_IMPUTE <- c(
    'post_count',
    'reputation',
    'reward_vesting_bal',
    'reward_vesting_steem',
    'voting_power',
    'votes',
    'polarity',
    'subjectivity',
    'days_since_last_post'
)
attrs[, VARS_TO_IMPUTE] <- apply(attrs[, VARS_TO_IMPUTE], 2, function(x) {
    return(as.numeric(ifelse(is.na(x), median(as.numeric(x), na.rm = TRUE), x)))
})
attrs$dom_pic_emotion <- ifelse(is.na(attrs$dom_pic_emotion), 'missing',
                                attrs$dom_pic_emotion)
net %v% 'Total Posts' <- attrs$post_count
net %v% 'Reputation' <- attrs$reputation
net %v% 'Reward Balance' <- attrs$reward_vesting_bal
net %v% 'Reward Steem' <- attrs$reward_vesting_steem
net %v% 'Voting Power' <- attrs$voting_power
net %v% 'Dominant Picture Emotion' <- attrs$dom_pic_emotion
net %v% 'Average Votes' <- attrs$votes
net %v% 'Polarity' <- attrs$polarity
net %v% 'Subjectivity' <- attrs$subjectivity
net %v% 'Days Since Last Post' <- attrs$days_since_last_post

# network statistics
density <- gden(net)
idegree <- degree(net, cmode = 'indegree')
odegree <- degree(net, cmode = 'outdegree')

mat <- igraph::graph.adjacency(as.matrix(net), mode = 'directed')
gn_results <- igraph::edge.betweenness.community(mat)
net %v% 'Community Membership' <- gn_results$membership

# graphs
coords <- coord_place(net)

pdf('polarity_graph.pdf', width=10, height=7.5)
    ggnet(net, shape = 'Dominant Picture Emotion', size = 'Reward Steem',
          color = 'Polarity', coords = coords, gradient = TRUE,
          legend = TRUE, title = 'Steemit Hot/Trending Network')
dev.off()
pdf('subjectivity_graph.pdf', width=10, height=7.5)
    ggnet(net, shape = 'Dominant Picture Emotion', size = 'Reward Steem',
          color = 'Subjectivity', coords = coords, gradient = TRUE,
          legend = TRUE, title = 'Steemit Hot/Trending Network')
dev.off()


# ergms
ergm_start <- ergm(net ~ edges + mutual + twopath + gwidegree(1) +
                   nodecov('Polarity') + nodecov('Subjectivity') +
                   nodecov('Total Posts') + nodefactor('Dominant Picture Emotion'),
                   control = control.ergm(MCMLE.maxit = 8))
params <- enformulate.curved(ergm_start)
ergm_final <- ergm(params$formula,
                   control = control.ergm(MCMLE.maxit = 15, MCMC.burnin = 50000,
                                          MCMC.interval = 1000, MCMC.samplesize = 10000))
