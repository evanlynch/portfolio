\ Model ReOrg
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  0 n[Michael,Michael] + n[Michael,Gina] + n[Gina,Michael] + 0 n[Gina,Gina]
   + 0 n[Matt,Matt] + n[Matt,Brenda] + n[Brenda,Matt] + 0 n[Brenda,Brenda]
Subject To
 assignment[Michael]: x[Michael,New_DepA] + x[Michael,New_DepB] = 1
 assignment[Gina]: x[Gina,New_DepA] + x[Gina,New_DepB] = 1
 assignment[Matt]: x[Matt,New_DepA] + x[Matt,New_DepB] = 1
 assignment[Brenda]: x[Brenda,New_DepA] + x[Brenda,New_DepB] = 1
 abEqualsba[Michael,Michael]: = 0
 abEqualsba[Michael,Gina]: n[Michael,Gina] - n[Gina,Michael] = 0
 abEqualsba[Michael,Matt]: n[Michael,Matt] - n[Matt,Michael] = 0
 abEqualsba[Michael,Brenda]: n[Michael,Brenda] - n[Brenda,Michael] = 0
 abEqualsba[Gina,Michael]: - n[Michael,Gina] + n[Gina,Michael] = 0
 abEqualsba[Gina,Gina]: = 0
 abEqualsba[Gina,Matt]: n[Gina,Matt] - n[Matt,Gina] = 0
 abEqualsba[Gina,Brenda]: n[Gina,Brenda] - n[Brenda,Gina] = 0
 abEqualsba[Matt,Michael]: - n[Michael,Matt] + n[Matt,Michael] = 0
 abEqualsba[Matt,Gina]: - n[Gina,Matt] + n[Matt,Gina] = 0
 abEqualsba[Matt,Matt]: = 0
 abEqualsba[Matt,Brenda]: n[Matt,Brenda] - n[Brenda,Matt] = 0
 abEqualsba[Brenda,Michael]: - n[Michael,Brenda] + n[Brenda,Michael] = 0
 abEqualsba[Brenda,Gina]: - n[Gina,Brenda] + n[Brenda,Gina] = 0
 abEqualsba[Brenda,Matt]: - n[Matt,Brenda] + n[Brenda,Matt] = 0
 abEqualsba[Brenda,Brenda]: = 0
Bounds
Binaries
 x[Michael,New_DepA] x[Michael,New_DepB] x[Gina,New_DepA] x[Gina,New_DepB]
 x[Matt,New_DepA] x[Matt,New_DepB] x[Brenda,New_DepA] x[Brenda,New_DepB]
 n[Michael,Michael] n[Michael,Gina] n[Michael,Matt] n[Michael,Brenda]
 n[Gina,Michael] n[Gina,Gina] n[Gina,Matt] n[Gina,Brenda] n[Matt,Michael]
 n[Matt,Gina] n[Matt,Matt] n[Matt,Brenda] n[Brenda,Michael] n[Brenda,Gina]
 n[Brenda,Matt] n[Brenda,Brenda]
General Constraints
 GC0: n[Michael,Gina] = AND ( x[Michael,New_DepA] )
 GC1: n[Michael,Gina] = AND ( x[Michael,New_DepB] )
 GC2: n[Michael,Matt] = AND ( x[Michael,New_DepA] )
 GC3: n[Michael,Matt] = AND ( x[Michael,New_DepB] )
 GC4: n[Michael,Brenda] = AND ( x[Michael,New_DepA] )
 GC5: n[Michael,Brenda] = AND ( x[Michael,New_DepB] )
 GC6: n[Gina,Michael] = AND ( x[Gina,New_DepA] )
 GC7: n[Gina,Michael] = AND ( x[Gina,New_DepB] )
 GC8: n[Gina,Matt] = AND ( x[Gina,New_DepA] )
 GC9: n[Gina,Matt] = AND ( x[Gina,New_DepB] )
 GC10: n[Gina,Brenda] = AND ( x[Gina,New_DepA] )
 GC11: n[Gina,Brenda] = AND ( x[Gina,New_DepB] )
 GC12: n[Matt,Michael] = AND ( x[Matt,New_DepA] )
 GC13: n[Matt,Michael] = AND ( x[Matt,New_DepB] )
 GC14: n[Matt,Gina] = AND ( x[Matt,New_DepA] )
 GC15: n[Matt,Gina] = AND ( x[Matt,New_DepB] )
 GC16: n[Matt,Brenda] = AND ( x[Matt,New_DepA] )
 GC17: n[Matt,Brenda] = AND ( x[Matt,New_DepB] )
 GC18: n[Brenda,Michael] = AND ( x[Brenda,New_DepA] )
 GC19: n[Brenda,Michael] = AND ( x[Brenda,New_DepB] )
 GC20: n[Brenda,Gina] = AND ( x[Brenda,New_DepA] )
 GC21: n[Brenda,Gina] = AND ( x[Brenda,New_DepB] )
 GC22: n[Brenda,Matt] = AND ( x[Brenda,New_DepA] )
 GC23: n[Brenda,Matt] = AND ( x[Brenda,New_DepB] )
End
