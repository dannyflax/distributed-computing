//
//  ViewController.m
//  Distrubutor
//
//  Created by Taha  on 10/16/15.
//  Copyright © 2015 OSUBoilerMaker. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    tcpHandler = [[TCP_Handler alloc] initWithDelegate:self];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)openconnection:(UIButton *)sender {
    if (!tcpHandler.connecting) {
        if (!tcpHandler.connected) {
            [tcpHandler connect];
        }
        else{
            [tcpHandler disconnect];
        }
    }
}

-(NSString *)performCalculation:(NSString *)data{
    if(![data containsString:@":"]){
        return @"Error";
    }
    else{
        NSArray *arr = [data componentsSeparatedByString:@":"];
        long lBound = [[arr objectAtIndex:0] integerValue];
        long uBound = [[arr objectAtIndex:1] integerValue];
        
        double sum = 0;
        for (long i = lBound; i<=uBound; i++) {
            sum+=pow((132.0/137.0), i);
        }
        return [NSString stringWithFormat:@"%.40f",sum];
    }
}

/** TCP_Delegate Methods **/

-(void)didConnect{
    NSLog(@"CONNECTED");
}

-(void)didDisconnect{
    NSLog(@"DISCONNECTED");
}

-(void)connectFailed{
    NSLog(@"FAILED TO CONNECT");
}

-(void)didReceiveCalculation:(NSString *)calculation{
    NSString *response = [self performCalculation:calculation];
    [tcpHandler writeAnswer:response];
}

@end
