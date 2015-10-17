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
            [self setConnectState:1];
            [tcpHandler connect];
        }
        else{
            [tcpHandler disconnect];
        }
    }
}

-(void)setConnectState:(int)state{
    NSString *title = @"";
    bool enabled = true;
    switch (state) {
        case 0:
            //Disconnected
            title = @"Connect";
            break;
        case 1:
            //Connecting
            title = @"Connecting...";
            enabled = false;
            break;
        case 2:
            //Connected
            title = @"Disconnect";
            break;
            
        default:
            break;
    }
    [connectButton setTitle:title forState:UIControlStateNormal];
    [connectButton setEnabled:enabled];
}

-(NSString *)performCalculation:(NSString *)data{
    if(![data containsString:@":"]){
        return @"Error";
    }
    else{
        NSArray *arr = [data componentsSeparatedByString:@":"];
        long indexOfDevice = [[arr objectAtIndex:0] integerValue];
        long deviceCount = [[arr objectAtIndex:1] integerValue];
        long uBound = [[arr objectAtIndex:2] integerValue];
        NSLog(@"deviceCount: %ld",deviceCount);
        double sum = 0;
        for (long i = indexOfDevice; i <= uBound; i+=deviceCount) {
            sum+=1;
        }
        
        return [NSString stringWithFormat:@"%f",sum];
    }
}

/** TCP_Delegate Methods **/

-(void)didConnect{
    NSLog(@"CONNECTED");
    [self setConnectState:2];
}

-(void)didDisconnect{
    NSLog(@"DISCONNECTED");
    [self setConnectState:0];
}

-(void)connectFailed{
    NSLog(@"FAILED TO CONNECT");
    [self setConnectState:0];
}

-(void)didReceiveCalculation:(NSString *)calculation{
    NSString *response = [self performCalculation:calculation];
    [tcpHandler writeAnswer:response];
}

@end
