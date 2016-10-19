#include <stdio.h>
#include <stdlib.h>

struct node
{
    int x;
    struct node *right;
    struct node *left;
};

struct btree
{
    struct node *root;
};

struct node * btree_create_node(int val)
{
    struct node *ptr = malloc(sizeof(*ptr));
    ptr->x = val;
    ptr->left = NULL;
    ptr->right = NULL;
    return ptr;
}

int node_insert(struct node *ptr, int val)
{
    if (val <= ptr->x)
    {
        if (ptr->left == NULL)
        {
            ptr->left = btree_create_node(val);
        }
        else
        {
            node_insert(ptr->left, val);
        }
    }
    else
    {
        if (ptr->right == NULL)
        {
            ptr->right = btree_create_node(val);
        }
        else
        {
            node_insert(ptr->right,val);
        }
    }

    return 0;
}

int btree_insert(struct btree *tree, int val)
{
    if (tree->root == NULL)
    {
        tree->root = btree_create_node(val);
    }
    else
    {
        node_insert(tree->root, val);
    }
    return 0;
}

int node_print(struct node * ptr)
{
    if (ptr->left != NULL)
    {
        node_print(ptr->left);
    }

    printf("%d", ptr->x);
    printf("\n");

    if (ptr->right != NULL)
    {
        node_print(ptr->right);
    }

    return 0;
}

int btree_print(struct btree *tree)
{

    if (tree->root == NULL)
    {
        return 0;
    }
    else
    {
        node_print(tree->root);
    }

    return 0;
}

int btree_delete_subtree(struct btree *tree, struct node *ptr)
{
    return 0;
}

struct btree *BTREE()
{
    struct btree *ptr = malloc(sizeof(*ptr));
    ptr->root = NULL;
    return ptr;
}

int main()
{
    struct btree tree = *BTREE();

    btree_insert(&tree, 43);
    btree_insert(&tree, 24);
    btree_insert(&tree, 14);
    btree_insert(&tree, 20);
    btree_insert(&tree, 100);
    btree_insert(&tree, 0);

    btree_print(&tree);

    return 0;
}
