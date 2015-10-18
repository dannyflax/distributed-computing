//
//  TCP_Handler.h
//  Distrubutor
//
//  Created by Danny Flax on 10/17/15.
//  Copyright © 2015 OSUBoilerMaker. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "CocoaAsyncSocket.h"
#import "TCP_Delegate.h"
@interface TCP_Handler : NSObject <GCDAsyncSocketDelegate>
{
    
}
-(void)connect;
-(void)disconnect;
-(void)writeAnswer:(NSString *)answer;
-(TCP_Handler *)initWithDelegate:(id<TCP_Delegate>)delegate;
@property (nonatomic) BOOL connected;
@property (nonatomic) BOOL connecting;
@property (nonatomic, strong) id<TCP_Delegate> delegate;
@property (nonatomic, strong) GCDAsyncSocket *socket;
@end
