#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 100

// A structure to represent a binary tree node
struct TreeNode {
    int data;
    struct TreeNode* left;
    struct TreeNode* right;
};

// A utility function to create a new binary tree node
struct TreeNode* newTreeNode(int data) {
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->data = data;
    node->left = node->right = NULL;
    return node;
}

// A function to build a binary tree from a given string
struct TreeNode* buildTree(char* str, int* index) {
    if (str[*index] == '\0' || str[*index] == ')')
        return NULL;

    int num = 0;
    while (str[*index] != '(' && str[*index] != ')' && str[*index] != '\0') {
        num = num * 10 + (str[*index] - '0');
        (*index)++;
    }

    struct TreeNode* root = newTreeNode(num);

    if (str[*index] == '(') {
        (*index)++;
        root->left = buildTree(str, index);
        (*index)++; // skip ')'
    }
    if (str[*index] == '(') {
        (*index)++;
        root->right = buildTree(str, index);
        (*index)++; // skip ')'
    }

    return root;
}

// A utility function to print the preorder traversal of a binary tree
void preOrder(struct TreeNode* node) {
    if (node == NULL)
        return;

    printf("%d ", node->data);
    preOrder(node->left);
    preOrder(node->right);
}

// Main function
int main() {
    char str[MAX] = "1(2(4)(5))(3(6)(7))";
    int index = 0;

    struct TreeNode* root = buildTree(str, &index);

    printf("Preorder Traversal of the constructed Binary Tree:\n");
    preOrder(root);
    printf("\n");

    return 0;
}
