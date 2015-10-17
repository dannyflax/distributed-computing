//
//  TCP_Delegate.h
//  Distributor
//
//  Created by Danny Flax on 10/17/15.
//  Copyright © 2015 OSUBoilerMaker. All rights reserved.
//

#ifndef TCP_Delegate_h
#define TCP_Delegate_h
@protocol TCP_Delegate
-(void)didConnect;
-(void)didDisconnect;
-(void)connectFailed;
-(void)didReceiveCalculation:(NSString *)calculation;
@end
#endif /* TCP_Delegate_h */
