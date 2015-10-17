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
    // Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)openconnection:(UIButton *)sender {
    [self disconnectconnection];
}

-(NSString *)performCalculation:(NSString *)data{
    if(![data containsString:@":"]){
        return @"Error";
    }
    else{
        NSArray *arr = [data componentsSeparatedByString:@":"];
        long lBound = [[arr objectAtIndex:0] integerValue];
        long uBound = [[arr objectAtIndex:1] integerValue];
        
        //We may want to switch to double later
        float sum = 0;
        for (long i = lBound; i<=uBound; i++) {
            sum+=pow(.2, i);
        }
        return [NSString stringWithFormat:@"%f",sum];
    }
}

- (void) disconnectconnection {
    printf("check");
}

@end
